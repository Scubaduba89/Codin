#!/usr/bin/env node
/* Conformance runner: the JS engine vs tests/fixture_events.json.
 * Mirrors tests/test_rules.py. Run from anywhere: node docs/js/run_fixture.js */
"use strict";
require("./rules.js");
require("./badges.js");
const fs = require("fs");
const path = require("path");

const fixture = JSON.parse(fs.readFileSync(
  path.join(__dirname, "..", "..", "tests", "fixture_events.json"), "utf8"));

const R = globalThis.CodinRules, B = globalThis.CodinBadges;
let failures = 0;

function caseLines(c) {
  if (c.events_raw) return c.events_raw;
  return c.events.map((e) => JSON.stringify(e));
}

function runCase(lines) {
  const parsed = R.parseLines(lines);
  const state = R.replay(parsed.events, fixture.curriculum);
  const earned = B.evaluate(fixture.badges, state);
  return { state, earned, ignored: parsed.ignored };
}

function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

for (const c of fixture.cases) {
  const { state, earned, ignored } = runCase(caseLines(c));
  const got = {
    xp: state.xp,
    level: state.level.number,
    badges: earned.map((b) => b.key).sort(),
    completed: state.completed_modules.slice().sort(),
    ignored,
  };
  const want = {
    xp: c.expect.xp,
    level: c.expect.level,
    badges: c.expect.badges.slice().sort(),
    completed: c.expect.completed_modules.slice().sort(),
    ignored: c.expect.ignored,
  };
  if (!eq(got, want)) {
    failures++;
    console.log("FAIL: " + c.name);
    console.log("  want " + JSON.stringify(want));
    console.log("  got  " + JSON.stringify(got));
  }
}

// file order must never matter
for (const c of fixture.cases) {
  if (c.events_raw) continue;
  const lines = caseLines(c);
  const shuffled = lines.slice().reverse();
  const a = runCase(lines), b = runCase(shuffled);
  if (a.state.xp !== b.state.xp ||
      !eq(a.earned.map((x) => x.key).sort(), b.earned.map((x) => x.key).sort())) {
    failures++;
    console.log("FAIL (order sensitivity): " + c.name);
  }
}

// level curve spot checks
const L = (xp) => R.levelFor(xp);
if (L(0).number !== 1 || L(39).number !== 1 || L(40).number !== 2 ||
    L(2300).number !== 14 || L(2675).name !== "Systems Mechanic I") {
  failures++;
  console.log("FAIL: level curve");
}

if (failures) {
  console.log(failures + " failure(s)");
  process.exit(1);
}
console.log("JS engine: all fixture cases green (" + fixture.cases.length + " cases)");
