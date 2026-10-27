"""FastAPI app: Bolna webhook, Guardian match-script tool, family alerts, dashboard."""

import logging
import re
from collections.abc import Callable
from dataclasses import asdict
from datetime import UTC, datetime
from functools import partial
from hmac import compare_digest
from pathlib import Path
from typing import Annotated, Any
from zoneinfo import ZoneInfo

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from scamkaki.domain import store, verdict
from scamkaki.domain.extraction import parse_extraction, parse_guardian_report
from scamkaki.domain.leaks import agent_turns, find_leaks
from scamkaki.domain.reports import draft_report
from scamkaki.domain.types import (
    Agency,
    Demand,
    GuardianReport,
    Language,
    as_language,
    as_line,
)
from scamkaki.integrations import telegram
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
# Bolna execution ids are UUIDs; anything else (an unfilled template) is dropped.
EXECUTION_ID = re.compile(r"[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}")

app = FastAPI(title="Scamkaki")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
templates.env.filters["sgt"] = lambda ts: ts.astimezone(SGT).strftime("%d %b %H:%M")

SettingsDep = Annotated[Settings, Depends(get_settings)]


basic = HTTPBasic(realm="Scamkaki admin")


def require_admin(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic)], settings: SettingsDep
) -> None:
    """Browser sign-in for the dashboard and web calls. Fails closed if no password is set."""
    ok_user = compare_digest(credentials.username.encode(), settings.admin_username.encode())
    ok_password = compare_digest(credentials.password.encode(), settings.admin_password.encode())
    if not settings.admin_password or not (ok_user and ok_password):
        raise HTTPException(
            status_code=401, headers={"WWW-Authenticate": 'Basic realm="Scamkaki admin"'}
        )


AdminDep = Depends(require_admin)


def get_bolna(settings: SettingsDep) -> BolnaClient:
    return BolnaClient(settings.bolna_api_key)


SendAlert = Callable[[str], bool]


def get_telegram(settings: SettingsDep) -> SendAlert | None:
    """The family's Telegram sender, or None when the bot is not configured."""
    if not (settings.telegram_bot_token and settings.telegram_chat_id):
        return None
    return partial(telegram.send_message, settings.telegram_bot_token, settings.telegram_chat_id)


def require_family_link(link_token: str, settings: SettingsDep) -> None:
    """The family page has no password; the secret link is the key. Fails closed if unset."""
    expected = settings.family_link_token
    if not expected or not compare_digest(link_token.encode(), expected.encode()):
        raise HTTPException(status_code=404)


FamilyDep = Depends(require_family_link)


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
    agent = settings.agent_line(execution.get("agent_id"))
    if agent is None:
        log.info("webhook for unknown agent ignored: %s", execution.get("agent_id"))
        return Response(status_code=204)
    line, language = agent
    transcript = execution.get("transcript") or ""
    extracted = execution.get("node_extracted_data") or execution.get("extracted_data") or {}
    fixture_case = fixture_case_of(execution)
    # The leak guard covers Ah Ma Bait, the persona that is asked for secrets.
    leaks = find_leaks(agent_turns(transcript)) if line == "bait" else []
    if leaks:
        log.warning("leak guard: %d leak(s) on execution %s", len(leaks), execution["id"])

    with connect(settings.database_url) as conn:
        call_id = store.upsert_call(
            conn,
            execution_id=str(execution["id"]),
            line=line,
            language=language,
            transcript=transcript,
            extracted=extracted,
            leaks=leaks,
            status=str(execution.get("status")),
            duration_s=execution.get("conversation_duration"),
            fixture_case=fixture_case,
        )
        if line == "bait":
            extraction = parse_extraction(extracted)
            store.add_script(conn, call_id, extraction)
            store.add_report(conn, call_id, draft_report(extraction, leaks, fixture_case))
    return Response(status_code=204)


@app.post("/tools/match-script")
async def match_script(
    request: Request,
    settings: SettingsDep,
    background: BackgroundTasks,
    send_alert: Annotated[SendAlert | None, Depends(get_telegram)],
) -> dict[str, Any]:
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
    report = parse_guardian_report(params)
    language = as_language(params.get("language"))
    execution_id = as_execution_id(params.get("execution_id"))

    try:
        similar_count = await run_in_threadpool(
            _count_similar, settings.database_url, report.agency, report.demand
        )
        result = verdict.match(report, similar_count, language)
    except Exception:
        log.exception("verdict failed; answering unclear")
        result = verdict.unclear(language)
    check_id = None
    try:
        check_id = await run_in_threadpool(
            _log_check, settings.database_url, report, language, result, execution_id
        )
    except Exception:
        # Never leave the senior in silence because logging failed.
        log.exception("failed to log guardian check")
    if result.verdict == "likely_scam":
        # Runs after the answer is sent, so a slow Telegram never delays Ah Ma.
        background.add_task(
            _alert_family,
            settings.database_url,
            send_alert,
            check_id,
            report,
            language,
            result.similar_count,
        )
    return asdict(result)


def as_execution_id(value: object) -> str | None:
    """The Bolna execution id the tool call carries, or None if Bolna left it unfilled."""
    text = str(value or "").strip()
    return text if EXECUTION_ID.fullmatch(text) else None


def _count_similar(database_url: str, agency: Agency, demand: Demand) -> int:
    with connect(database_url) as conn:
        return store.count_similar(conn, agency, demand)


def _log_check(database_url: str, report, language, result, execution_id) -> int:
    with connect(database_url) as conn:
        return store.log_guardian_check(conn, report, language, result, execution_id)


def _alert_family(
    database_url: str,
    send_alert: SendAlert | None,
    check_id: int | None,
    report: GuardianReport,
    language: Language,
    similar_count: int,
) -> None:
    if send_alert is None:
        status = "off"
    else:
        text = verdict.alert_text(report, language, similar_count, datetime.now(UTC))
        status = "sent" if send_alert(text) else "failed"
    if check_id is None:
        return
    try:
        with connect(database_url) as conn:
            store.set_alert_status(conn, check_id, status)
    except Exception:
        log.exception("failed to record family alert status")


@app.get("/family/{link_token}", response_class=HTMLResponse, dependencies=[FamilyDep])
def family_page(request: Request) -> HTMLResponse:
    response = templates.TemplateResponse(
        request,
        "family.html",
        {
            "agencies": verdict.AGENCY_LABELS,
            "demands": verdict.DEMAND_LABELS,
            "channels": verdict.CHANNEL_LABELS,
            "tactics": verdict.TACTIC_LABELS,
            "acted": verdict.ACTED_LABELS,
            "languages": verdict.LANGUAGE_LABELS,
        },
    )
    # Keep the secret link out of Referer headers and search engines.
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Robots-Tag"] = "noindex"
    return response


@app.get("/family/{link_token}/alerts", dependencies=[FamilyDep])
def family_alerts(settings: SettingsDep, response: Response) -> list[dict[str, Any]]:
    response.headers["Cache-Control"] = "no-store"
    with connect(settings.database_url) as conn:
        rows = store.recent_alerts(conn)
    return [{**row, "created_at": row["created_at"].isoformat()} for row in rows]


@app.post("/web-call/session", dependencies=[AdminDep])
async def web_call_session(
    request: Request,
    settings: SettingsDep,
    bolna: Annotated[BolnaClient, Depends(get_bolna)],
    language: str = "en",
    line: str = "guardian",
) -> dict[str, Any]:
    agent_id = settings.agent_id(as_line(line), as_language(language))
    if not agent_id:
        raise HTTPException(status_code=503, detail="Agent not configured")
    # The Web Call SDK posts {} or {"user_data": {...}}; pass only string variables on.
    try:
        body = await request.json()
    except ValueError:
        body = {}
    user_data = body.get("user_data") if isinstance(body, dict) else None
    if isinstance(user_data, dict):
        user_data = {str(k): str(v) for k, v in user_data.items()}
    else:
        user_data = None
    return await run_in_threadpool(bolna.mint_web_call_session, agent_id, user_data)


@app.get("/", response_class=HTMLResponse, dependencies=[AdminDep])
def dashboard(request: Request, settings: SettingsDep) -> HTMLResponse:
    with connect(settings.database_url) as conn:
        calls = store.recent_calls(conn)
        checks = store.recent_checks(conn)
        scripts = store.recent_scripts(conn)
    return templates.TemplateResponse(
        request, "dashboard.html", {"calls": calls, "checks": checks, "scripts": scripts}
    )
