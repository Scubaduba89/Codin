# SPEC.md — The Codin Engine Contract

This file is **normative**. Two engines implement it — the Python CLI
(`engine/rules.py`, `engine/badges.py`) and the dashboard
(`docs/js/rules.js`, `docs/js/badges.js`) — and both must produce
identical results for any input. `tests/fixture_events.json` is the
shared conformance fixture; a change to this spec is not done until both
engines pass the fixture again.

Nothing in this file is about *how* things are displayed. It defines the
data and the math.

---

## 1. The event log

Progress lives in **`docs/data/events.jsonl`**: one JSON object per
line, UTF-8, LF line endings, **append-only**. Nothing ever edits or
deletes a line; every number shown anywhere (XP, level, badges, module
completion) is recomputed from this log plus the curriculum index. The
file is committed, and `.gitattributes` gives it `merge=union` so
appends from two devices never conflict.

### 1.1 Event schema (v1)

```json
{"v":1,"uid":"a1f4c9d02b7e","ts":"2026-08-23T19:04:11Z","device":"desktop","type":"pass","id":"terminal-a2-03","xp":10}
```

| field | meaning |
|---|---|
| `v` | schema version, always `1` |
| `uid` | first 12 hex chars of `sha256("<type>\n<id>\n<ts>\n<device>")` (UTF-8) |
| `ts` | UTC time, ISO-8601 with `Z`, seconds precision |
| `device` | the device name chosen in `codin doctor` (e.g. `desktop`, `phone`) |
| `type` | `pass` \| `quiz` \| `review` \| `gate` \| `stage` \| `milestone` |
| `id` | see table below |
| `xp` | integer XP this event claims |

| type | `id` refers to | when appended |
|---|---|---|
| `pass` | an exercise id (`terminal-a2-03`) | `codin check` succeeds |
| `quiz` | a module id (`terminal-a1`) | first `codin quiz` pass at ≥ 80% |
| `review` | a review item id (`review:<module>:<qkey>`) | a due spaced-review item answered correctly |
| `gate` | a gate exercise id (`gate-p1`) | `codin gate` succeeds |
| `stage` | `<project exercise id>#<stage>` (`c-f7-01#2`) | a project stage's checklist passes |
| `milestone` | a workshop milestone id (`workshop-m1-01`) | a workshop milestone's check passes |

Only the CLI appends events. Humans and tutors never write this file by
hand.

---

## 2. Replay: from log to numbers

Both engines implement exactly this algorithm.

1. **Parse.** Read lines in file order. Skip blank lines. Skip lines
   that are not valid JSON or lack any of the seven fields (count them,
   report them as `ignored`, never crash).
2. **Dedupe.** Keep the first occurrence of each `uid`; drop the rest.
   (Union merges can duplicate whole lines.)
3. **Sort.** Order events by `(ts, uid)` ascending. File order is not
   chronological after a two-device merge; sorted order is the one
   truth.
4. **Count XP.** Walk the sorted events. An event *counts* by type:
   - `review`: always counts (reviews are repeatable by design).
   - every other type: counts only if no earlier event with the same
     `(type, id)` already counted — an exercise's XP is earned once,
     earliest event wins. Passing the same exercise on two devices
     before a sync is therefore a harmless no-op, not a conflict.
5. **Module completion.** A module is *complete* when it has at least
   one exercise in the curriculum index and every one of its exercise
   ids has a counted `pass` (or `gate`) event. Modules with zero
   exercises (stubs) are never complete. Quiz events are bonus XP and do
   **not** gate completion.
6. **Module bonus.** Each completed module whose `module.json` does not
   set `"no_bonus": true` contributes a virtual bonus (no event is
   written):
   `bonus = round_to_5(0.4 × sum of the module's exercise xp values)`
   where `round_to_5(x) = floor(x / 5 + 0.5) × 5`. The bonus's
   timestamp, where one is needed (badges, timeline), is the `ts` of the
   event that completed the module.
7. **Total XP** = sum of counted events' `xp` + sum of module bonuses.

### 2.1 Levels

Level = the highest row whose threshold ≤ total XP. The learner is
Level 1 from the moment the log exists, even empty.

| lvl | XP | name | | lvl | XP | name |
|---|---|---|---|---|---|---|
| 1 | 0 | Spark | | 8 | 725 | Data Wrangler |
| 2 | 40 | Terminal Tenant | | 9 | 925 | Query Author |
| 3 | 100 | Navigator | | 10 | 1150 | Webwright |
| 4 | 180 | Pipeline Plumber | | 11 | 1400 | Compiler Wrangler |
| 5 | 280 | Daily Committer | | 12 | 1675 | Pointer Prover |
| 6 | 400 | Script Writer | | 13 | 1975 | Syscall Witness |
| 7 | 550 | Pythonista | | 14 | 2300 | Shellwright's Apprentice |

From level 15 on, each level costs a flat **+375 XP**
(15 → 2675, 16 → 3050, …) and is named **Systems Mechanic I, II, III…**
(roman numeral = level − 14).

Progress bars are always scoped: "XP into current level / XP to next
level" or "exercises done in this module". Neither engine ever computes
"% of curriculum".

### 2.2 XP economy (informative)

Values live in each exercise's `meta.json`; this table is the authoring
convention, not a runtime rule: micro 10 · standard 25 · challenge 50 ·
project stage 40 · project completion 100 · quiz first pass 15 · due
review item 5 · gate 50 · workshop milestone 100 · module bonus 40%
(rounded to 5). No decay, no multipliers, no loss, ever.

---

## 3. Badges

Badges are **derived, never stored**. Definitions live in
`docs/data/badges.json` (one shared file, read by both engines);
adding a rule there awards it retroactively from history — replaying old
events through new rules is a feature, not a bug.

```json
{"key":"first-commit","name":"First Commit","tier":"moment","icon":"✦",
 "desc":"You made a commit with your own hands.","rule":{"kind":"exercise","id":"setup-02"}}
```

`tier` ∈ `moment` | `power` | `artifact` | `spirit`.

### 3.1 Rule kinds

Rules evaluate over the **deduped, sorted** event list (step 3 above)
and the curriculum index. `earned_ts` is the `ts` of the event that
completed the rule.

| kind | fields | fires when |
|---|---|---|
| `first_event` | — | the first counted `pass` event exists |
| `exercise` | `id` | a counted `pass`/`gate`/`milestone` event for `id` exists |
| `exercises_all` | `ids` | every id in `ids` has a counted `pass`/`gate`/`milestone` event |
| `modules_all` | `ids` | every listed module is complete (§2 step 5) |
| `devices` | `count` | deduped events name ≥ `count` distinct devices (any type — the phone event proves the phone) |
| `gap_return` | `days` | some deduped event's `ts` is ≥ `days` × 86400 s after the latest `ts` before it |

An engine that meets an unknown `kind` ignores that badge (forward
compatibility for M4, where new kinds may be invented).

---

## 4. Spaced review

The review pool is derived; no separate state file.

- **Items**: every question in `quizzes/<module>.json` of every module
  whose quiz has a counted `quiz` event. Item id:
  `review:<module>:<qkey>`.
- **Intervals**: `2, 7, 21, 60` days.
- An item's anchor is the `ts` of its latest `review` event, or of the
  module's `quiz` event if it has never been reviewed. With `n` prior
  review events, the item is **due** when
  `now ≥ anchor + intervals[min(n, 3)]`.
- A correct answer to a due item appends a `review` event (5 XP). Items
  answered while not due earn nothing and append nothing.

---

## 5. Practice record

An **active day** is a UTC calendar date on which at least one counted
XP event exists. The record is presented positively only ("active 4 of
the last 7 days"); no mechanic anywhere may reference commit counts,
missed days, or broken chains.

---

## 6. Conformance

`tests/fixture_events.json` is hermetic: it carries its own mini
curriculum, its own badge definitions, and a list of cases
(`events` → expected `xp`, `level`, `badges`, `completed_modules`).

- Python: `python3 -m unittest tests.test_rules` must pass.
- JS: `node docs/js/run_fixture.js` must pass, and `docs/test.html`
  runs the same cases in any browser.

Both engines must also satisfy: replaying any *prefix* of a case's
events never yields more XP than the full case, and replaying a case's
events in any file order yields identical results.
