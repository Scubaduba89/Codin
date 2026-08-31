"""codin next - always exactly one suggestion.

Honors gates (module/exercise requires), the advisory WIP limit,
session length on the phone, and the re-entry ramp. Never proposes a
list; choosing from menus is the platform's job, not the learner's.
"""

from datetime import datetime, timezone

from . import content, state as state_mod

GAP_DAYS = 7


def _days_since_last(replay_state):
    evs = replay_state["events"]
    if not evs:
        return None
    last = evs[-1]["ts"]
    then = datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - then).days


def suggest(curriculum, replay_state, local, phone=False, minutes=None, due_reviews=0):
    """-> {"kind": "exercise", "exercise": ex, "why": str}
        | {"kind": "review", "due": n, "why": str}
        | {"kind": "done", "why": str}
    """
    gap = _days_since_last(replay_state)
    if gap is not None and gap >= GAP_DAYS and due_reviews > 0:
        return {
            "kind": "review", "due": due_reviews,
            "why": "Welcome back. A %d-minute warm-up: your due reviews." % min(due_reviews * 2, 10),
        }

    done = replay_state["done"]
    parked = set(local.get("parked", []))
    started = local.get("started", {})
    in_progress_modules = []
    for ex_id in started:
        kind, ex = content.find(curriculum, ex_id)
        if kind == "exercise" and ex["module"] not in in_progress_modules:
            in_progress_modules.append(ex["module"])

    def candidates():
        # In-progress (non-parked) modules first, then curriculum order.
        mods = sorted(
            curriculum["modules"],
            key=lambda m: (m["id"] not in in_progress_modules, m["phase"], m["order"]),
        )
        for mod in mods:
            if mod["id"] in parked or not mod["exercises"]:
                continue
            for ex in mod["exercises"]:
                if ex["id"] in done:
                    continue
                ok, _unmet = content.unlocked(curriculum, ex, replay_state)
                if ok:
                    yield ex

    for ex in candidates():
        if phone:
            if not ex.get("phone"):
                continue
            if minutes and ex.get("minutes", 0) > minutes:
                continue
        why = "next in %s" % ex["module"]
        if ex["module"] in in_progress_modules:
            why = "continuing %s" % ex["module"]
        return {"kind": "exercise", "exercise": ex, "why": why}

    if phone:
        if due_reviews > 0:
            return {"kind": "review", "due": due_reviews,
                    "why": "nothing phone-sized is unlocked, but reviews are always phone-sized"}
        for ex in candidates():  # honest fallback: ignore the phone filter
            return {"kind": "exercise", "exercise": ex,
                    "why": "heads-up: this one is better done at the desk"}

    if due_reviews > 0:
        return {"kind": "review", "due": due_reviews,
                "why": "everything unlocked is done - reviews keep it warm"}
    return {"kind": "done",
            "why": "Nothing unlocked is unfinished. Time to open the next gate."}
