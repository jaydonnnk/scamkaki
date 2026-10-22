"""FastAPI app: Bolna webhook, Guardian match-script tool, dashboard."""

import logging
from dataclasses import asdict
from hmac import compare_digest
from pathlib import Path
from typing import Annotated, Any
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from scamkaki.domain import store
from scamkaki.domain.types import Line, as_agency, as_demand
from scamkaki.domain.verdict import stub_match
from scamkaki.integrations.bolna import BolnaClient
from scamkaki.lib.db import connect
from scamkaki.lib.env import Settings, get_settings

log = logging.getLogger("scamkaki")

# Statuses after which the execution is final; "call-disconnected" still has empty fields.
TERMINAL_STATUSES = {
    "completed",
    "no-answer",
    "busy",
    "failed",
    "canceled",
    "stopped",
    "error",
    "balance-low",
}
SGT = ZoneInfo("Asia/Singapore")

app = FastAPI(title="Scamkaki")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
templates.env.filters["sgt"] = lambda ts: ts.astimezone(SGT).strftime("%d %b %H:%M")

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_bolna(settings: SettingsDep) -> BolnaClient:
    return BolnaClient(settings.bolna_api_key)


def line_for(agent_id: str | None, settings: Settings) -> Line | None:
    if agent_id and agent_id == settings.bolna_guardian_agent_id:
        return "guardian"
    if agent_id and agent_id == settings.bolna_bait_agent_id:
        return "bait"
    return None


def fixture_case_of(execution: dict[str, Any]) -> str | None:
    context = execution.get("context_details") or {}
    recipient = context.get("recipient_data") or {}
    value = recipient.get("fixture_case") or context.get("fixture_case")
    return str(value) if value else None


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.post("/bolna/webhook/{token}", status_code=204)
def bolna_webhook(
    token: str,
    payload: dict[str, Any],
    settings: SettingsDep,
    bolna: Annotated[BolnaClient, Depends(get_bolna)],
) -> Response:
    if not compare_digest(token, settings.bolna_webhook_token):
        raise HTTPException(status_code=404)
    execution_id = payload.get("id")
    if not execution_id:
        raise HTTPException(status_code=422, detail="missing execution id")
    if payload.get("status") not in TERMINAL_STATUSES:
        return Response(status_code=204)

    # Re-read the execution from Bolna rather than trusting the posted body.
    execution = bolna.get_execution(str(execution_id))
    line = line_for(execution.get("agent_id"), settings)
    if line is None:
        log.info("webhook for unknown agent ignored: %s", execution.get("agent_id"))
        return Response(status_code=204)

    with connect(settings.database_url) as conn:
        store.upsert_call(
            conn,
            execution_id=str(execution["id"]),
            line=line,
            transcript=execution.get("transcript") or "",
            extracted=execution.get("node_extracted_data") or execution.get("extracted_data") or {},
            status=str(execution.get("status")),
            duration_s=execution.get("conversation_duration"),
            fixture_case=fixture_case_of(execution),
        )
    return Response(status_code=204)


@app.post("/tools/match-script")
async def match_script(request: Request, settings: SettingsDep) -> dict[str, Any]:
    expected = f"Bearer {settings.bolna_tool_token}"
    if not compare_digest(request.headers.get("authorization", ""), expected):
        raise HTTPException(status_code=401)
    try:
        body = await request.json()
    except ValueError:
        body = {}
    if not isinstance(body, dict):
        body = {}
    params = {**request.query_params, **body}
    agency, demand = as_agency(params.get("agency")), as_demand(params.get("demand"))

    result = stub_match()
    try:
        await run_in_threadpool(_log_check, settings.database_url, agency, demand, result)
    except Exception:
        # Never leave the senior in silence because logging failed.
        log.exception("failed to log guardian check")
    return asdict(result)


def _log_check(database_url: str, agency, demand, result) -> None:
    with connect(database_url) as conn:
        store.log_guardian_check(conn, agency, demand, result)


@app.post("/web-call/session")
def web_call_session(
    settings: SettingsDep, bolna: Annotated[BolnaClient, Depends(get_bolna)]
) -> dict[str, Any]:
    if not settings.bolna_guardian_agent_id:
        raise HTTPException(status_code=503, detail="Guardian agent not configured")
    return bolna.mint_web_call_session(settings.bolna_guardian_agent_id)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, settings: SettingsDep) -> HTMLResponse:
    with connect(settings.database_url) as conn:
        calls = store.recent_calls(conn)
        checks = store.recent_checks(conn)
    return templates.TemplateResponse(request, "dashboard.html", {"calls": calls, "checks": checks})
