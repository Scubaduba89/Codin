"""Unit tests for sandbox/checker/quiz/review mechanics using a
synthetic exercise in a temp repo - no real curriculum content needed."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import checkers, content, quiz, review, rules, sandbox

CHECK_PY = '''
def setup(ctx):
    (ctx.box / "seed.txt").write_text("planted\\n")

def check(ctx):
    ctx.require(ctx.exists("done.txt"), "expected `done.txt` in the sandbox")
    ctx.require("hello" in ctx.read("done.txt"), "done.txt should say hello")
'''

STAGED_CHECK_PY = '''
def _stage1(ctx):
    ctx.require(ctx.exists("s1.txt"), "expected s1.txt")

def _stage2(ctx):
    ctx.require(ctx.exists("s2.txt"), "expected s2.txt")

STAGES = [("first", _stage1), ("second", _stage2)]

def check(ctx):
    ctx.require(ctx.exists("final.txt"), "expected final.txt")
'''


def make_repo(tmp):
    root = Path(tmp)
    exdir = root / "curriculum" / "testtrack" / "t1" / "01-hello"
    exdir.mkdir(parents=True)
    (exdir.parent / "module.json").write_text(json.dumps({
        "id": "test-t1", "track": "testtrack", "title": "Test", "phase": 1,
        "order": 1, "summary": "s"}))
    (exdir / "meta.json").write_text(json.dumps({
        "id": "test-t1-01", "title": "Hello", "type": "micro",
        "minutes": 5, "phone": True, "xp": 10}))
    (exdir / "check.py").write_text(CHECK_PY)
    fix = exdir / "fixture"
    fix.mkdir()
    (fix / "given.txt").write_text("from fixture\n")

    ex2 = exdir.parent / "02-project"
    ex2.mkdir()
    (ex2 / "meta.json").write_text(json.dumps({
        "id": "test-t1-02", "title": "Proj", "type": "project",
        "minutes": 90, "phone": False, "xp": 100}))
    (ex2 / "check.py").write_text(STAGED_CHECK_PY)

    (root / "quizzes").mkdir()
    (root / "quizzes" / "test-t1.json").write_text(json.dumps({
        "module": "test-t1",
        "questions": [
            {"key": "q1", "q": "2+2?", "choices": ["3", "4"], "answer": 1},
            {"key": "q2", "q": "cmd?", "answer_sha": checkers.sha_norm("Pwd")},
        ]}))
    (root / "docs" / "data").mkdir(parents=True)
    return root


class TestCheckers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = make_repo(self.tmp)
        self.curr = content.load_curriculum(self.root)
        self.ex = content.exercise_map(self.curr)["test-t1-01"]

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_sandbox_fixture_and_setup(self):
        checker = checkers.load_checker(self.root, self.ex)
        box, created = sandbox.materialize(self.root, self.ex, checker)
        self.assertTrue(created)
        self.assertEqual((box / "given.txt").read_text(), "from fixture\n")
        self.assertEqual((box / "seed.txt").read_text(), "planted\n")
        # idempotent
        _, created2 = sandbox.materialize(self.root, self.ex, checker)
        self.assertFalse(created2)

    def test_check_fail_then_pass(self):
        checker = checkers.load_checker(self.root, self.ex)
        box, _ = sandbox.materialize(self.root, self.ex, checker)
        with self.assertRaises(checkers.CheckFail) as cm:
            checkers.run_check(self.root, self.ex, checker, box)
        self.assertIn("done.txt", str(cm.exception))
        (box / "done.txt").write_text("hello world\n")
        ok, _ = checkers.run_check(self.root, self.ex, checker, box)
        self.assertTrue(ok)

    def test_reset_rebuilds(self):
        checker = checkers.load_checker(self.root, self.ex)
        box, _ = sandbox.materialize(self.root, self.ex, checker)
        (box / "junk.txt").write_text("x")
        box, _ = sandbox.reset(self.root, self.ex, checker)
        self.assertFalse((box / "junk.txt").exists())
        self.assertTrue((box / "seed.txt").exists())

    def test_stages(self):
        ex2 = content.exercise_map(self.curr)["test-t1-02"]
        checker = checkers.load_checker(self.root, ex2)
        stages = checkers.stage_list(checker)
        self.assertEqual([s[0] for s in stages], ["first", "second"])
        box, _ = sandbox.materialize(self.root, ex2, checker)
        with self.assertRaises(checkers.CheckFail):
            stages[0][1](checkers.Ctx(self.root, ex2, box))
        (box / "s1.txt").write_text("x")
        stages[0][1](checkers.Ctx(self.root, ex2, box))  # no raise

    def test_timeout_is_friendly(self):
        checker = checkers.load_checker(self.root, self.ex)
        box, _ = sandbox.materialize(self.root, self.ex, checker)
        ctx = checkers.Ctx(self.root, self.ex, box)
        with self.assertRaises(checkers.CheckFail) as cm:
            ctx.run([sys.executable, "-c", "while True: pass"], timeout=1)
        self.assertIn("infinite loop", str(cm.exception))


class TestQuizAndReview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = make_repo(self.tmp)
        self.curr = content.load_curriculum(self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_grading(self):
        bank = quiz.load_bank(self.root, "test-t1")
        mc, exact = bank["questions"]
        self.assertTrue(quiz.grade(mc, "b"))
        self.assertFalse(quiz.grade(mc, "a"))
        self.assertIsNone(quiz.grade(mc, "elephant"))
        self.assertTrue(quiz.grade(exact, "  PWD "))
        self.assertFalse(quiz.grade(exact, "ls"))

    def test_review_schedule(self):
        def ev(uid, ts, etype, eid, xp):
            return {"v": 1, "uid": uid, "ts": ts, "device": "d",
                    "type": etype, "id": eid, "xp": xp}

        quiz_pass = ev("u1", "2026-01-01T12:00:00Z", "quiz", "test-t1", 15)
        st = rules.replay([quiz_pass], self.curr)
        day = 86400.0
        t0 = review._epoch("2026-01-01T12:00:00Z")
        # not due after 1 day, due after 2
        self.assertEqual(len(review.due_items(self.root, self.curr, st, now=t0 + day)), 0)
        self.assertEqual(len(review.due_items(self.root, self.curr, st, now=t0 + 2 * day)), 2)
        # reviewing one item moves only that item to the 7-day interval
        r1 = ev("u2", "2026-01-03T12:00:00Z", "review", "review:test-t1:q1", 5)
        st2 = rules.replay([quiz_pass, r1], self.curr)
        due = review.due_items(self.root, self.curr, st2, now=t0 + 3 * day)
        self.assertEqual([d[0] for d in due], ["review:test-t1:q2"])
        due7 = review.due_items(self.root, self.curr, st2, now=t0 + 2 * day + 7 * day)
        self.assertIn("review:test-t1:q1", [d[0] for d in due7])


if __name__ == "__main__":
    unittest.main()
