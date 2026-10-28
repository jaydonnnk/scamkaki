// Offline check of the page's real script. No microphone, network, Bolna SDK or credit use.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(process.argv[2] || new URL("index.html", import.meta.url), "utf8");
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
const elements = new Map();
const element = (id) => {
  if (!elements.has(id)) elements.set(id, {
    value: "", textContent: "", hidden: false, disabled: false, children: [],
    add(option) { this.children.push(option); if (!this.value) this.value = option.value; },
    appendChild(child) { this.children.push(child); },
    replaceChildren() { this.children = []; },
  });
  return elements.get(id);
};
let clipFetches = 0;
const records = [], timers = new Map(), instances = [];
const nativeMicrophone = () => { throw new Error("Offline test must not request a microphone"); };
const facts = [{ id: "en-ica-video-01", line: "guardian", language: "en",
  label: "Demo fixture: role-play", senior_lines: ["ICA called.", "Moved to video.", "Yes."],
  clips: ["/clips/never-play.wav"] }];
class OfflineCall {
  constructor(options) { this.options = options; this.listeners = {}; instances.push(this); }
  on(name, handler) { this.listeners[name] = handler; }
  start() { this.state = "active"; this.listeners["call-start"](); }
  stop() { this.state = "ended"; this.listeners["call-end"]({ reason: "offline-stop" }); }
  getRunId() { return "offline-roleplay-test"; }
  getState() { return this.state; }
}
const sandbox = {
  document: { getElementById: element, createElement: () => ({ textContent: "" }) },
  Option: class { constructor(text, value) { this.text = text; this.value = value; } },
  navigator: { mediaDevices: { getUserMedia: nativeMicrophone } },
  AudioContext: class { constructor() { throw new Error("Live mode created synthetic audio"); } },
  BolnaWebCall: OfflineCall,
  setTimeout: (fn, ms) => { const id = timers.size + 1; timers.set(id, { fn, ms }); return id; },
  clearTimeout: (id) => timers.delete(id),
  fetch: async (url, options) => {
    if (url === "/cases") return { json: async () => facts };
    if (url === "/log") { records.push(JSON.parse(options.body)); return {}; }
    clipFetches++; throw new Error("Live mode fetched an audio clip");
  },
};
vm.runInNewContext(script, sandbox, { filename: "caller/index.html" });
await new Promise(setImmediate);
element("case").value = "guardian:en-ica-video-01";
element("mode").value = "live";
element("case").onchange?.();
await element("start").onclick();
await new Promise(setImmediate);
assert.equal(clipFetches, 0);
assert.equal(sandbox.navigator.mediaDevices.getUserMedia, nativeMicrophone);
assert.equal(instances.length, 1);
assert.match(instances[0].options.sessionUrl, /case=en-ica-video-01/);
assert.match(instances[0].options.sessionUrl, /mode=live/);
assert.equal(element("case").disabled, true);
assert.equal(element("mode").disabled, true);
assert.equal(instances[0].getState(), "active", "Live call ended without the operator");
assert.deepEqual([...timers.values()].map((t) => t.ms), [180000]);
await element("stop").onclick();
await new Promise(setImmediate);
assert.equal(records[0].case, "en-ica-video-01");
assert.equal(records[0].caller_mode, "live");
assert.equal(records[0].caller_kind, "human_roleplay");
assert.equal(records[0].clips_played, 0);
assert.equal(element("start").disabled, false);
assert.equal(sandbox.navigator.mediaDevices.getUserMedia, nativeMicrophone);
assert.equal(timers.size, 0);

// The only automatic live-mode hang-up is the duration cap.
await element("start").onclick();
await new Promise(setImmediate);
[...timers.values()][0].fn();
await new Promise(setImmediate);
assert.equal(instances[1].getState(), "ended");
assert.equal(records.length, 2);
console.log("PASS: live microphone preserved, no clips or timing-driven replies, fixture id and mode logged, operator/cap hang-up checked. No real calls.");
