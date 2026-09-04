"""Spaced review per SPEC.md §4 - the guaranteed phone command.

Pool: every question of every module whose quiz has been passed.
Intervals 2/7/21/60 days; each due item answered correctly appends a
5 XP review event. The whole scheduler is derived from the event log -
there is no separate state to sync or lose.
"""

from datetime import datetime, timezone

from . import sync as sync_mod
from . import events, quiz as quiz_mod, state, ui

INTERVALS_DAYS = [2, 7, 21, 60]
REVIEW_XP = 5
SESSION_CAP = 10


def _epoch(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc).timestamp()


def due_items(repo_root, curriculum, replay_state, now=None):
    """-> [(item_id, module_id, question)] due right now."""
    now = now or datetime.now(timezone.utc).timestamp()
    quiz_ts = {
        ev["id"]: ev["ts"]
        for ev in replay_state["counted"] if ev["type"] == "quiz"
    }
    reviews = {}
    for ev in replay_state["events"]:
        if ev["type"] == "review":
            reviews.setdefault(ev["id"], []).append(ev["ts"])

    due = []
    for module_id, passed_ts in quiz_ts.items():
        bank = quiz_mod.load_bank(repo_root, module_id)
        if not bank:
            continue
        for q in bank["questions"]:
            item = "review:%s:%s" % (module_id, q["key"])
            hist = sorted(reviews.get(item, []))
            anchor = hist[-1] if hist else passed_ts
            interval = INTERVALS_DAYS[min(len(hist), len(INTERVALS_DAYS) - 1)]
            if now >= _epoch(anchor) + interval * 86400:
                due.append((item, module_id, q))
    return due


def run(repo_root, curriculum, replay_state):
    due = due_items(repo_root, curriculum, replay_state)
    if not due:
        ui.say("Nothing due. Reviews unlock 2 days after you pass a "
               "module quiz - and that's a feature, not a queue.")
        return 0
    device = state.device_name(repo_root) or "unknown"
    ui.headline("Review — %d due (capped at %d per sitting)" %
                (len(due), SESSION_CAP))
    earned = 0
    for item, module_id, q in due[:SESSION_CAP]:
        ok, _ = quiz_mod.ask(q)
        if ok:
            events.append(repo_root, "review", item, REVIEW_XP, device)
            earned += REVIEW_XP
            ui.say(ui.c("  ✔ +%d XP" % REVIEW_XP, "green"))
        elif "choices" in q:
            ui.say(ui.c("  ✘ it's %s) %s - it'll come around again" % (
                "abcdefgh"[q["answer"]], q["choices"][q["answer"]]), "yellow"))
        else:
            ui.say(ui.c("  ✘ not it - it'll come around again", "yellow"))
    ui.say("")
    ui.say(ui.c("  Session done: +%d XP." % earned, "green", "bold"))
    if len(due) > SESSION_CAP:
        ui.say("  (%d more due - another sitting, another day.)" %
               (len(due) - SESSION_CAP))
    for line in sync_mod.nudge_lines(repo_root):
        ui.say(ui.c("  " + line, "dim"))
    return 0
