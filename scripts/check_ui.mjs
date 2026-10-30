// Execute the owning UI scripts offline. No browser SDK, microphone, network or credit use.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const templates = new URL("../src/scamkaki/app/templates/", import.meta.url);
const voice = readFileSync(new URL("voice.html", templates), "utf8");
const overview = readFileSync(new URL("dashboard.html", templates), "utf8");
const inline = (html) => [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
const tick = () => new Promise(setImmediate);

function room({ missingSDK = false, startMode = "pending", stopMode = "end" } = {}) {
  const elements = new Map();
  const element = (id) => {
    if (!elements.has(id)) {
      const e = { value: "", textContent: "", disabled: false, hidden: false, dataset: {} };
      Object.defineProperty(e, "innerHTML", { set() { throw new Error("Unsafe HTML write"); } });
      elements.set(id, e);
    }
    return elements.get(id);
  };
  const radios = ["guardian", "bait"].map((id) => Object.assign(element(id), {
    value: id, checked: id === "guardian", dataset: { en: "true", hi: "true" },
  }));
  element("language").value = "en";
  element("start").disabled = true;
  element("hang-up").disabled = true;
  element("voice-results").hidden = true;
  const instances = [], timers = [], events = {};
  const counts = { constructors: 0, starts: 0, stops: 0, reloads: 0, microphones: 0, fetches: 0 };
  const modes = { start: startMode, stop: stopMode };
  class FakeCall {
    constructor(options) {
      counts.constructors++;
      if (modes.start === "constructor-throw") throw new Error("Constructor unavailable");
      this.options = options;
      this.handlers = {};
      instances.push(this);
    }
    on(name, handler) { this.handlers[name] = handler; }
    emit(name, value) { this.handlers[name]?.(value); }
    start() {
      counts.starts++;
      if (modes.start === "throw") throw new Error("Start threw");
      if (modes.start === "reject") return Promise.reject(new Error("Start rejected"));
      if (modes.start === "sync-error") {
        this.emit("error", { message: "Synchronous error" });
        return Promise.reject(new Error("Synchronous error"));
      }
      return new Promise((resolve, reject) => { this.resolveStart = resolve; this.rejectStart = reject; });
    }
    connect() { this.emit("call-start"); this.resolveStart?.(); }
    stop() {
      counts.stops++;
      if (modes.stop === "reject") return Promise.reject(new Error("Stop rejected"));
      if (modes.stop === "pending") return new Promise((resolve) => { this.resolveStop = resolve; });
      this.emit("call-end");
      return Promise.resolve();
    }
  }
  const body = {};
  const document = {
    body, activeElement: body, getElementById: element,
    querySelectorAll: () => radios,
    querySelector: () => radios.find((r) => r.checked),
    addEventListener: (name, handler) => { events[name] = handler; },
  };
  const sandbox = {
    document, window: { addEventListener: (name, handler) => { events[name] = handler; } },
    location: { reload() { counts.reloads++; } },
    navigator: { mediaDevices: { getUserMedia() { counts.microphones++; throw new Error("Real mic requested"); } } },
    fetch() { counts.fetches++; throw new Error("Real fetch requested"); },
    setInterval: (fn, ms) => { timers.push({ fn, ms }); },
    setTimeout: (fn, ms) => { timers.push({ fn, ms }); },
  };
  if (!missingSDK) sandbox.BolnaWebCall = FakeCall;
  vm.runInNewContext(inline(voice), sandbox, { filename: "voice.html" });
  const select = (line, language) => {
    radios.forEach((r) => { r.checked = r.value === line; });
    element("language").value = language;
    radios.find((r) => r.checked).onchange?.();
    element("language").onchange?.();
  };
  return { element, radios, counts, instances, timers, modes, sandbox, document, events, select };
}

const tests = {
  async "explicit-start"() {
    const r = room();
    r.select("bait", "hi"); r.select("guardian", "en");
    assert.deepEqual(r.counts, { constructors: 0, starts: 0, stops: 0, reloads: 0, microphones: 0, fetches: 0 });
    assert.equal(r.timers.length, 0, "Voice installed automatic timers");
    assert.equal(r.element("start").disabled, false);
    assert.equal(typeof r.element("start").onclick, "function");
  },
  async "one-at-a-time-and-selection-lock"() {
    const r = room(); r.select("bait", "hi");
    r.element("start").onclick(); r.element("start").onclick();
    assert.equal(r.counts.constructors, 1); assert.equal(r.counts.starts, 1);
    assert.equal(r.instances[0].options.sessionUrl, "/web-call/session?line=bait&language=hi");
    assert.equal(r.element("language").disabled, true);
    assert.ok(r.radios.every((e) => e.disabled));
    assert.equal(r.element("start").disabled, true);
    assert.equal(r.element("hang-up").disabled, false);
    assert.match(r.element("voice-status").textContent, /Connecting/);
    r.instances[0].connect(); await tick();
    assert.match(r.element("voice-status").textContent, /Connected/);
    assert.ok(r.radios.every((e) => e.disabled));
  },
  async "natural-end-and-restart"() {
    const r = room(); r.element("start").onclick(); r.instances[0].connect(); await tick();
    r.instances[0].emit("call-end"); await tick();
    assert.equal(r.element("start").disabled, false);
    assert.equal(r.element("language").disabled, false);
    assert.ok(r.radios.every((e) => !e.disabled));
    assert.equal(r.element("hang-up").disabled, true);
    assert.equal(r.element("voice-results").hidden, false);
    assert.match(r.element("voice-status").textContent, /ended/i);
    r.element("start").onclick();
    assert.equal(r.instances.length, 2); assert.equal(r.counts.starts, 2);
    assert.equal(r.element("voice-results").hidden, true);
    assert.equal(r.counts.reloads, 0); assert.equal(r.timers.length, 0);
  },
  async "hang-up-during-connection"() {
    const r = room({ stopMode: "pending" }); r.element("start").onclick();
    r.element("hang-up").onclick(); r.element("hang-up").onclick(); await tick();
    r.element("start").onclick();
    assert.equal(r.counts.starts, 1); assert.equal(r.counts.stops, 1);
    assert.equal(r.element("language").disabled, true);
    r.instances[0].emit("call-start");
    assert.doesNotMatch(r.element("voice-status").textContent, /Connected/);
    r.instances[0].resolveStop(); await tick();
    assert.equal(r.element("start").disabled, false);
    assert.match(r.element("voice-status").textContent, /ended/i);
  },
  async "hang-up-connected"() {
    const r = room(); r.element("start").onclick(); r.instances[0].connect(); await tick();
    await r.element("hang-up").onclick(); await tick();
    assert.equal(r.counts.stops, 1); assert.equal(r.element("start").disabled, false);
    assert.equal(r.element("voice-results").hidden, false);
  },
  ...Object.fromEntries(["constructor-throw", "throw", "reject", "sync-error"].map((mode) => [
    `failure-${mode}`, async () => {
      const r = room({ startMode: mode }); await r.element("start").onclick(); await tick();
      assert.equal(r.element("start").disabled, false);
      assert.equal(r.element("language").disabled, false);
      assert.ok(r.radios.every((e) => !e.disabled));
      assert.match(r.element("voice-status").textContent, /Could not connect/);
      r.modes.start = "pending"; r.element("start").onclick();
      assert.equal(r.element("start").disabled, true);
      assert.equal(r.counts.starts, mode === "constructor-throw" ? 1 : 2);
    },
  ])),
  async "error-stops-before-recovery"() {
    const r = room({ stopMode: "pending" }); r.element("start").onclick();
    r.instances[0].emit("error", { message: "Connection lost" }); await tick();
    r.element("start").onclick();
    assert.equal(r.counts.starts, 1); assert.equal(r.counts.stops, 1);
    r.instances[0].resolveStop(); await tick();
    assert.equal(r.element("start").disabled, false);
    assert.match(r.element("voice-status").textContent, /Could not connect: Connection lost/);
  },
  async "stop-failure-keeps-attempt-locked-for-retry"() {
    const r = room({ stopMode: "reject" }); r.element("start").onclick();
    await r.element("hang-up").onclick(); await tick();
    assert.equal(r.element("start").disabled, true);
    assert.equal(r.element("language").disabled, true);
    assert.equal(r.element("hang-up").disabled, false);
    assert.match(r.element("voice-status").textContent, /Could not hang up/);
    r.modes.stop = "end"; await r.element("hang-up").onclick(); await tick();
    assert.equal(r.element("start").disabled, false);
  },
  ...Object.fromEntries(["call-start", "call-end", "error", "rejection"].map((event) => [
    `late-${event}`, async () => {
      const r = room(); r.element("start").onclick(); const old = r.instances[0];
      old.emit("call-end"); r.select("bait", "hi"); r.element("start").onclick();
      if (event === "rejection") old.rejectStart(new Error("Late start rejection"));
      else old.emit(event, { message: "Late error" });
      await tick();
      assert.equal(r.counts.starts, 2); assert.equal(r.counts.stops, 0);
      assert.equal(r.element("start").disabled, true);
      assert.equal(r.element("language").disabled, true);
      assert.match(r.element("voice-status").textContent, /Connecting/);
      r.instances[1].connect(); await tick();
      assert.match(r.element("voice-status").textContent, /Connected/);
    },
  ])),
  async "unavailable-selection"() {
    for (const [line, language] of [["guardian", "en"], ["guardian", "hi"], ["bait", "en"], ["bait", "hi"]]) {
      const r = room(); r.element(line).dataset[language] = "false"; r.select(line, language);
      assert.equal(r.element("start").disabled, true);
      assert.match(r.element("voice-availability").textContent, /not configured/);
      r.element("start").onclick(); assert.equal(r.counts.starts, 0);
      r.select(line === "bait" ? "guardian" : "bait", language);
      assert.equal(r.element("start").disabled, false);
    }
  },
  async "missing-sdk"() {
    const r = room({ missingSDK: true });
    assert.equal(r.element("start").disabled, true);
    assert.match(r.element("voice-availability").textContent, /could not load/i);
    r.element("start").onclick(); assert.equal(r.counts.starts, 0);
  },
  async "error-is-text"() {
    const r = room(); r.element("start").onclick();
    r.instances[0].emit("error", { message: '<img src=x onerror="steal()">' }); await tick();
    assert.equal(r.element("voice-status").textContent, 'Could not connect: <img src=x onerror="steal()">');
    assert.equal(r.element("start").disabled, false);
  },
  async "overview-focus-refresh-without-call-owner"() {
    const r = room();
    vm.runInNewContext(inline(overview), r.sandbox, { filename: "dashboard.html" });
    assert.equal(r.counts.starts, 0); assert.equal(r.counts.constructors, 0);
    assert.equal(r.timers.length, 1); assert.equal(r.timers[0].ms, 15000);
    r.document.activeElement = r.element("focus-control"); r.timers[0].fn();
    assert.equal(r.counts.reloads, 0);
    assert.match(r.element("refresh").textContent, /paused/);
    r.document.activeElement = r.document.body; r.timers[0].fn();
    assert.equal(r.counts.reloads, 1);
  },
};

const only = process.argv[2];
if (only && !tests[only]) throw new Error(`Unknown UI check: ${only}`);
let passed = 0;
for (const [name, check] of Object.entries(tests)) {
  if (only && name !== only) continue;
  try { await check(); passed++; }
  catch (error) { console.error(`FAIL ${name}\n${error.stack}`); process.exitCode = 1; }
}
if (!process.exitCode) console.log(`PASS ${passed} offline UI checks. Actual owning scripts, fake SDK/DOM, zero real microphone/network/provider use.`);
