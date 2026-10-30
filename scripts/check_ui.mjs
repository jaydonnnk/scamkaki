// Execute the owning UI scripts offline. No browser SDK, microphone, network or credit use.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const templates = new URL("../src/scamkaki/app/templates/", import.meta.url);
const voice = readFileSync(new URL("voice.html", templates), "utf8");
const family = readFileSync(new URL("family.html", templates), "utf8");
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


// Render the actual Family script's Jinja dictionaries with controlled labels.
const familyLabels = {
  agencies: {courier: "Courier", bank: "Bank"}, demands: {card_details: "Card details on a website"},
  channels: {sms: "SMS"}, tactics: {link_fee: "Small fee by link"},
  acted: {paid: "Paid", gave_code_or_card: "Shared a code or card details", none: "Not acted"},
  languages: {en: "English", hi: "Hindi हिंदी"},
};
const familyScript = inline(family).replace(/{{ (\w+) \| tojson }}/g, (_, name) => {
  assert.ok(Object.hasOwn(familyLabels, name), `Uncontrolled Family label map ${name}`);
  return JSON.stringify(familyLabels[name]);
});
assert.doesNotMatch(familyScript, /{{|{%/, "Family harness left unrendered Jinja");
const alertFixture = (id = 1, fields = {}) => ({
  id, agency: "courier", demand: "card_details", channel: "sms", tactics: ["link_fee"],
  acted: "gave_code_or_card", urgent: true, language: "hi", similar_count: 2,
  alert_status: "sent", created_at: "2026-10-30T02:00:00Z", ...fields,
});
function familyRoom(initial = []) {
  let document;
  let now = Date.parse("2026-10-30T02:01:00Z");
  class Node {
    constructor(tag) { this.tagName = tag; this.children = []; this.attributes = {}; this.className = ""; this.handlers = {}; this.ownText = ""; this.parentElement = null; this.open = false; }
    set textContent(value) { this.replaceChildren(); this.ownText = String(value); }
    get textContent() { return this.ownText + this.children.map((n) => typeof n === "string" ? n : n.textContent).join(""); }
    set innerHTML(_) { throw new Error("Unsafe Family HTML write"); }
    detach(node) {
      if (!node || typeof node === "string") return;
      for (let active = document?.activeElement; active; active = active.parentElement) {
        if (active === node) { document.activeElement = document.body; break; }
      }
      if (node.parentElement) node.parentElement.children = node.parentElement.children.filter((n) => n !== node);
      node.parentElement = null;
    }
    append(...nodes) {
      for (const node of nodes) { this.detach(node); if (typeof node !== "string") node.parentElement = this; this.children.push(node); }
    }
    replaceChildren(...nodes) { for (const node of [...this.children]) this.detach(node); this.children = []; this.ownText = ""; this.append(...nodes); }
    get isConnected() { let node = this; while (node.parentElement) node = node.parentElement; return node === document?.body; }
    focus() { document.activeElement = this; }
    setAttribute(name, value) { this.attributes[name] = value; }
    addEventListener(name, fn) { this.handlers[name] = fn; }
    get classList() { return { remove: (name) => { this.className = this.className.split(" ").filter((s) => s !== name).join(" "); } }; }
  }
  const elements = new Map(["latest", "earlier", "status", "sound"].map((id) => [id, new Node("div")]));
  const nodes = () => [...elements.values()].flatMap(function walk(n) { return [n, ...n.children.filter((x) => typeof x !== "string").flatMap(walk)]; });
  const counts = {fetches: 0, audio: 0, tones: 0};
  const intervals = [], timeouts = [], responses = [initial], paths = [], events = {};
  document = {
    body: new Node("body"),
    title: "Ah Ma Guardian family alerts", hidden: false,
    getElementById: (id) => { assert.ok(elements.has(id), `Unexpected Family ID ${id}`); return elements.get(id); },
    createElement: (tag) => new Node(tag),
    querySelectorAll: (selector) => nodes().filter((n) => selector.split(",").some((part) => n.className.split(" ").includes(part.trim().replace(".", "")))),
    addEventListener: (name, fn) => { events[name] = fn; },
  };
  document.activeElement = document.body; document.body.append(...elements.values());
  class FakeDate extends Date { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return now; } }
  class FakeAudio {
    constructor() { counts.audio++; this.currentTime = 0; this.destination = {}; }
    createOscillator() { return {frequency: {}, connect: (target) => target, start: () => { counts.tones++; }, stop: () => {}}; }
    createGain() { return {gain: {}, connect: () => this.destination}; }
  }
  const sandbox = {
    document, Date: FakeDate, AudioContext: FakeAudio,
    location: {pathname: "/family/synthetic-private/"},
    fetch: async (url, options) => {
      counts.fetches++; paths.push({url, options}); const response = responses.shift();
      if (response instanceof Error) throw response;
      return {ok: response !== "http-error", status: 503, json: async () => response};
    },
    setInterval: (fn, ms) => { intervals.push({fn, ms}); },
    setTimeout: (fn, ms) => { const task = {fn, at: now + ms}; timeouts.push(task); return task; },
    clearTimeout: (task) => { if (task) task.cancelled = true; },
  };
  vm.runInNewContext(familyScript, sandbox, {filename: "family.html"});
  return {
    counts, document, events, paths, intervals, nodes,
    text: (id) => elements.get(id).textContent,
    attribute: (id, name) => elements.get(id).attributes[name],
    async poll(response) { responses.push(response); await intervals[0].fn(); await tick(); },
    async advance(ms) { now += ms; for (const t of timeouts.splice(0)) { if (!t.cancelled && t.at <= now) t.fn(); else timeouts.push(t); } await tick(); },
    sound() { const target = elements.get("sound"); target.handlers.click({target}); },
  };
}

const tests = {
  async "family-initial-empty-and-poll-path"() {
    const r = familyRoom(); await tick();
    assert.match(r.text("latest"), /No alerts yet/); assert.equal(r.text("earlier"), "None.");
    assert.deepEqual(r.intervals.map((t) => t.ms), [5000]);
    assert.equal(r.paths[0].url, "/family/synthetic-private/alerts");
    assert.equal(r.paths[0].options.cache, "no-store");
    assert.deepEqual(r.counts, {fetches: 1, audio: 0, tones: 0});
  },
  async "family-first-load-is-quiet"() {
    const r = familyRoom([alertFixture(), alertFixture(2, {urgent: false})]); await tick();
    assert.match(r.text("latest"), /Urgent: Ah Ma already acted/);
    assert.match(r.text("latest"), /Likely scam/); assert.match(r.text("latest"), /Hindi हिंदी/);
    assert.match(r.text("latest"), /Call Ah Ma now. Help her call the bank on the number on the back of her card./);
    assert.match(r.text("latest"), /Same script heard 2 times this week./);
    assert.match(r.text("earlier"), /Courier/);
    assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 0);
    assert.equal(r.counts.audio, 0); assert.equal(r.counts.tones, 0);
    assert.equal(r.document.title, "Ah Ma Guardian family alerts");
  },
  async "family-successful-empty-clears-all-alerts"() {
    const r = familyRoom([alertFixture(), alertFixture(2)]); await tick();
    await r.poll([]);
    assert.match(r.text("latest"), /No alerts yet/); assert.doesNotMatch(r.text("latest"), /Likely scam|Courier/);
    assert.equal(r.text("earlier"), "None."); assert.doesNotMatch(r.text("status"), /stale|out of date|Cannot reach/);
    assert.equal(r.document.title, "Ah Ma Guardian family alerts");
  },
  async "family-failure-retains-stale-and-recovers"() {
    const r = familyRoom([alertFixture(), alertFixture(2)]); await tick();
    const before = r.text("latest"), earlier = r.text("earlier");
    for (const failure of [new Error("offline"), "http-error"]) {
      await r.poll(failure); assert.equal(r.text("latest"), before); assert.equal(r.text("earlier"), earlier);
      assert.match(r.text("status"), /out of date|stale/i); assert.match(r.text("status"), /Trying again/);
    }
    await r.poll([alertFixture(1, {alert_status: "failed"})]);
    assert.doesNotMatch(r.text("status"), /out of date|stale|Cannot reach/i);
    assert.match(r.text("latest"), /Telegram: failed/); assert.equal(r.counts.tones, 0);
  },
  async "family-initial-failure-is-unavailable"() {
    const r = familyRoom(new Error("offline")); await tick();
    assert.match(r.text("status"), /unavailable/i);
    await r.poll([alertFixture()]);
    assert.match(r.text("latest"), /Likely scam/); assert.equal(r.counts.tones, 0);
    assert.equal(r.nodes().filter((n) => n.className.includes("flash")).length, 0);
  },
  async "family-hostile-values-are-text"() {
    const needle = '<img src=x onerror="syntheticNeedle()">';
    const a = alertFixture(1, {agency: needle, demand: needle, channel: needle, tactics: [needle], acted: needle, language: needle});
    const r = familyRoom([a, {...a, id: 2}]); await tick();
    assert.ok(r.text("latest").includes(needle)); assert.ok(r.text("earlier").includes(needle));
    assert.ok(r.nodes().every((n) => !["img", "script"].includes(n.tagName)));
  },
  async "family-prototype-keys-remain-text"() {
    const r = familyRoom([alertFixture(1, {agency: "constructor", demand: "toString", channel: "__proto__", tactics: ["constructor"], acted: "toString", language: "__proto__"})]); await tick();
    const values = r.nodes().filter((n) => n.tagName === "strong").map((n) => n.textContent);
    for (const value of ["constructor", "toString", "__proto__"]) assert.ok(values.includes(value), `Recorded value lost: ${value}`);
  },
  async "family-missing-fields-and-nonurgent-guidance"() {
    const r = familyRoom([{id: 1}]); await tick();
    assert.match(r.text("latest"), /Please call Ah Ma now./);
    assert.match(r.text("latest"), /Not recorded/);
    assert.doesNotMatch(r.text("latest"), /undefined|null|Invalid Date|already acted|Same script/);
    assert.match(r.text("latest"), /Telegram: unknown/);
    assert.ok(r.nodes().some((n) => n.tagName === "details"));
    assert.ok(r.nodes().some((n) => n.tagName === "summary" && /Why Guardian/.test(n.textContent)));
  },
  async "family-sent-is-not-receipt"() {
    const r = familyRoom([alertFixture()]); await tick();
    assert.match(r.text("latest"), /Telegram: sent/);
    assert.match(r.text("latest"), /does not confirm.*received or read/i);
  },
  async "family-new-alert-without-sound"() {
    const r = familyRoom([]); await tick(); await r.poll([alertFixture()]);
    assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 1);
    assert.equal(r.document.title, "Likely scam call - Ah Ma Guardian");
    assert.equal(r.counts.audio, 0); assert.equal(r.counts.tones, 0);
    r.events.visibilitychange(); assert.equal(r.document.title, "Ah Ma Guardian family alerts");
  },
  async "family-sound-opt-in-and-seen-alerts"() {
    const r = familyRoom([alertFixture()]); await tick(); r.sound();
    assert.equal(r.counts.audio, 1); assert.equal(r.counts.tones, 3);
    assert.equal(r.attribute("sound", "aria-pressed"), "true"); assert.equal(r.text("sound"), "Sound on");
    await r.poll([alertFixture(2), alertFixture()]); assert.equal(r.counts.tones, 6);
    await r.poll([alertFixture(2)]); assert.equal(r.counts.tones, 6);
    await r.poll([]); await r.poll([alertFixture(2)]); assert.equal(r.counts.tones, 6);
    r.sound(); await r.poll([alertFixture(3)]); assert.equal(r.counts.tones, 6);
    assert.equal(r.attribute("sound", "aria-pressed"), "false"); assert.equal(r.text("sound"), "Turn on sound");
  },
  async "family-flash-stops-without-successful-poll"() {
    const r = familyRoom([]); await tick(); await r.poll([alertFixture()]);
    await r.poll(new Error("offline")); await r.advance(30000);
    assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 0);
    assert.match(r.text("latest"), /Likely scam/); assert.match(r.text("status"), /out of date|stale/i);
  },
  async "family-empty-stops-flashing"() {
    const r = familyRoom([]); await tick(); await r.poll([alertFixture()]); await r.poll([]);
    assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 0);
    assert.match(r.text("latest"), /No alerts yet/);
    assert.equal(r.document.title, "Ah Ma Guardian family alerts");
  },
  async "family-unchanged-poll-preserves-disclosures"() {
    const data = [alertFixture(), alertFixture(2)];
    const r = familyRoom(data); await tick();
    const latest = r.nodes().find((n) => n.tagName === "section");
    const disclosure = r.nodes().find((n) => n.tagName === "details");
    disclosure.open = true;
    await r.poll(data);
    assert.equal(r.nodes().find((n) => n.tagName === "section"), latest);
    assert.equal(r.nodes().find((n) => n.tagName === "details"), disclosure);
    assert.equal(disclosure.open, true);
  },
  async "family-serializes-polls-until-success"() {
    let release; const pending = new Promise((resolve) => { release = resolve; });
    const r = familyRoom(pending); await tick();
    await r.poll([alertFixture(2)]);
    assert.equal(r.counts.fetches, 1, "Overlapping poll was issued");
    release([]); await tick(); assert.match(r.text("latest"), /No alerts yet/);
    await r.intervals[0].fn(); await tick();
    assert.equal(r.counts.fetches, 2); assert.match(r.text("latest"), /Likely scam/);
    assert.doesNotMatch(r.text("status"), /unavailable|out of date/);
  },
  async "family-serializes-polls-until-failure-and-unlocks"() {
    let reject; const pending = new Promise((_, fail) => { reject = fail; });
    const r = familyRoom(pending); await tick();
    await r.poll([alertFixture(2)]); assert.equal(r.counts.fetches, 1);
    reject(new Error("Delayed old failure")); await tick();
    assert.match(r.text("status"), /unavailable/);
    await r.intervals[0].fn(); await tick();
    assert.equal(r.counts.fetches, 2); assert.match(r.text("latest"), /Likely scam/);
    assert.doesNotMatch(r.text("status"), /unavailable|out of date/);
  },
  async "family-status-update-preserves-open-focused-reasons"() {
    const first = [alertFixture(1, {alert_status: "pending"}), alertFixture(2)];
    for (const index of [0, 1]) {
      const r = familyRoom(first); await tick();
      const details = r.nodes().filter((n) => n.tagName === "details");
      details.forEach((n) => { n.open = true; }); const focused = details[index].children[0]; focused.focus();
      await r.poll([alertFixture(), alertFixture(2, {alert_status: "failed"})]);
      const after = r.nodes().filter((n) => n.tagName === "details");
      assert.equal(after[0], details[0]); assert.equal(after[1], details[1]);
      assert.ok(after.every((n) => n.open)); assert.equal(r.document.activeElement, focused);
      assert.ok(focused.isConnected); assert.match(r.text("latest"), /Telegram: sent/);
    }
  },
  async "family-addition-and-reorder-preserve-focused-alert"() {
    const r = familyRoom([alertFixture(1), alertFixture(2)]); await tick();
    const details = r.nodes().filter((n) => n.tagName === "details");
    details.forEach((n) => { n.open = true; }); const focused = details[0].children[0]; focused.focus();
    await r.poll([alertFixture(3), alertFixture(2), alertFixture(1)]);
    const moved = r.nodes().filter((n) => n.tagName === "details");
    assert.equal(moved[2], details[0]); assert.equal(moved[1], details[1]);
    assert.equal(moved[2].open, true); assert.equal(moved[1].open, true);
    assert.equal(r.document.activeElement, focused); assert.ok(focused.isConnected);
    await r.poll([]); assert.equal(focused.isConnected, false);
  },
  async "family-date-rollover-refreshes-without-losing-focus"() {
    const data = [alertFixture()]; const r = familyRoom(data); await tick();
    const details = r.nodes().find((n) => n.tagName === "details"); details.open = true;
    const focused = details.children[0]; focused.focus();
    await r.advance(24 * 60 * 60 * 1000); await r.poll(data);
    assert.doesNotMatch(r.text("latest"), /Today/); assert.match(r.text("latest"), /Fri, 30 Oct/);
    assert.equal(r.nodes().find((n) => n.tagName === "details"), details);
    assert.equal(details.open, true); assert.equal(r.document.activeElement, focused);
    assert.equal(r.counts.tones, 0);
  },
  async "family-flash-deadline-and-no-retrigger"() {
    const r = familyRoom([]); await tick(); await r.poll([alertFixture()]);
    await r.advance(29999); assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 1);
    await r.advance(1); assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 0);
    await r.poll([alertFixture()]); assert.equal(r.nodes().filter((n) => n.className.split(" ").includes("flash")).length, 0);
  },
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
