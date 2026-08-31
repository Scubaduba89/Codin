"""Conformance: engine/rules.py + engine/badges.py vs the shared fixture.

docs/js/run_fixture.js runs the same cases through the JS engine; both
must agree with the hand-computed expectations, per SPEC.md §6.
"""

import json
import random
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import badges, events, rules

FIXTURE = json.loads(
    (Path(__file__).parent / "fixture_events.json").read_text(encoding="utf-8")
)


def case_lines(case):
    if "events_raw" in case:
        return case["events_raw"]
    return [json.dumps(ev) for ev in case["events"]]


def run_case(lines, curriculum, badge_defs):
    parsed, ignored = events.parse_lines(lines)
    state = rules.replay(parsed, curriculum)
    earned = badges.evaluate(badge_defs, state)
    return state, earned, ignored


class TestFixtureCases(unittest.TestCase):
    def test_all_cases(self):
        for case in FIXTURE["cases"]:
            with self.subTest(case=case["name"]):
                state, earned, ignored = run_case(
                    case_lines(case), FIXTURE["curriculum"], FIXTURE["badges"]
                )
                expect = case["expect"]
                self.assertEqual(state["xp"], expect["xp"])
                self.assertEqual(state["level"]["number"], expect["level"])
                self.assertEqual(
                    sorted(b["key"] for b in earned), sorted(expect["badges"])
                )
                self.assertEqual(
                    sorted(state["completed_modules"]),
                    sorted(expect["completed_modules"]),
                )
                self.assertEqual(ignored, expect["ignored"])

    def test_file_order_never_matters(self):
        rng = random.Random(42)
        for case in FIXTURE["cases"]:
            if "events_raw" in case:
                continue
            lines = case_lines(case)
            for _ in range(5):
                shuffled = lines[:]
                rng.shuffle(shuffled)
                state, earned, _ = run_case(
                    shuffled, FIXTURE["curriculum"], FIXTURE["badges"]
                )
                self.assertEqual(state["xp"], case["expect"]["xp"], case["name"])
                self.assertEqual(
                    sorted(b["key"] for b in earned),
                    sorted(case["expect"]["badges"]),
                    case["name"],
                )

    def test_prefix_monotonicity(self):
        for case in FIXTURE["cases"]:
            if "events_raw" in case:
                continue
            lines = case_lines(case)
            prev_xp = 0
            for cut in range(len(lines) + 1):
                state, _, _ = run_case(
                    lines[:cut], FIXTURE["curriculum"], FIXTURE["badges"]
                )
                self.assertGreaterEqual(state["xp"], prev_xp, case["name"])
                prev_xp = state["xp"]

    def test_level_curve(self):
        self.assertEqual(rules.level_for(0)["number"], 1)
        self.assertEqual(rules.level_for(39)["number"], 1)
        self.assertEqual(rules.level_for(40)["number"], 2)
        self.assertEqual(rules.level_for(2299)["number"], 13)
        self.assertEqual(rules.level_for(2300)["number"], 14)
        self.assertEqual(rules.level_for(2674)["number"], 14)
        self.assertEqual(rules.level_for(2675)["name"], "Systems Mechanic I")
        self.assertEqual(rules.level_for(3050)["name"], "Systems Mechanic II")
        # next_threshold is always strictly ahead
        for xp in (0, 39, 40, 2299, 2300, 2675, 9999):
            lv = rules.level_for(xp)
            self.assertLessEqual(lv["threshold"], xp)
            self.assertGreater(lv["next_threshold"], xp)

    def test_real_badge_defs_are_well_formed(self):
        repo = Path(__file__).resolve().parent.parent
        defs = badges.load_defs(repo)
        self.assertGreaterEqual(len(defs), 25)
        known_kinds = {
            "first_event", "exercise", "exercises_all",
            "modules_all", "devices", "gap_return",
        }
        keys = set()
        for b in defs:
            for field in ("key", "name", "tier", "icon", "desc", "rule"):
                self.assertIn(field, b, b.get("key", "?"))
            self.assertIn(b["tier"], {"moment", "power", "artifact", "spirit"})
            self.assertIn(b["rule"]["kind"], known_kinds, b["key"])
            self.assertNotIn(b["key"], keys)
            keys.add(b["key"])
        # empty log earns nothing
        state = rules.replay([], {"modules": []})
        self.assertEqual(badges.evaluate(defs, state), [])

    def test_uid_shape(self):
        uid = events.make_uid("pass", "setup-01", "2026-08-23T19:00:00Z", "desktop")
        self.assertEqual(len(uid), 12)
        int(uid, 16)  # raises if not hex


if __name__ == "__main__":
    unittest.main()
