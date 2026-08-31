"""The pure fold from event log to numbers. Mirrors SPEC.md §2 exactly.

docs/js/rules.js implements the same spec for the dashboard; both must
pass tests/fixture_events.json. No I/O in this module.
"""

LEVELS = [
    (1, 0, "Spark"),
    (2, 40, "Terminal Tenant"),
    (3, 100, "Navigator"),
    (4, 180, "Pipeline Plumber"),
    (5, 280, "Daily Committer"),
    (6, 400, "Script Writer"),
    (7, 550, "Pythonista"),
    (8, 725, "Data Wrangler"),
    (9, 925, "Query Author"),
    (10, 1150, "Webwright"),
    (11, 1400, "Compiler Wrangler"),
    (12, 1675, "Pointer Prover"),
    (13, 1975, "Syscall Witness"),
    (14, 2300, "Shellwright's Apprentice"),
]
EXTRA_LEVEL_XP = 375

# Counted events of these types mark an exercise as done for module
# completion and badge purposes.
DONE_TYPES = ("pass", "gate", "milestone")


def _roman(n):
    out = []
    for value, glyph in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= value:
            out.append(glyph)
            n -= value
    return "".join(out)


def level_for(xp):
    """-> {number, name, threshold, next_threshold}"""
    top_num, top_xp, _ = LEVELS[-1]
    if xp >= top_xp + EXTRA_LEVEL_XP:
        extra = (xp - top_xp) // EXTRA_LEVEL_XP
        num = top_num + extra
        return {
            "number": num,
            "name": "Systems Mechanic " + _roman(extra),
            "threshold": top_xp + extra * EXTRA_LEVEL_XP,
            "next_threshold": top_xp + (extra + 1) * EXTRA_LEVEL_XP,
        }
    current = LEVELS[0]
    nxt = None
    for row in LEVELS:
        if xp >= row[1]:
            current = row
        elif nxt is None:
            nxt = row
    return {
        "number": current[0],
        "name": current[2],
        "threshold": current[1],
        "next_threshold": nxt[1] if nxt else top_xp + EXTRA_LEVEL_XP,
    }


def round_to_5(x):
    return int(x / 5 + 0.5) * 5


def dedupe_sort(events):
    """SPEC §2 steps 2-3: first occurrence per uid, then sort by (ts, uid)."""
    seen, out = set(), []
    for ev in events:
        if ev["uid"] in seen:
            continue
        seen.add(ev["uid"])
        out.append(ev)
    out.sort(key=lambda ev: (ev["ts"], ev["uid"]))
    return out


def replay(raw_events, curriculum):
    """SPEC §2: fold parsed events (file order) + curriculum into state.

    curriculum: {"modules": [{"id", "no_bonus"?, "exercises": [{"id","xp"}]}]}
    """
    events = dedupe_sort(raw_events)

    counted = []
    counted_keys = set()
    done = {}  # exercise id -> counting event (pass/gate/milestone)
    for ev in events:
        if ev["type"] == "review":
            counted.append(ev)
            continue
        key = (ev["type"], ev["id"])
        if key in counted_keys:
            continue
        counted_keys.add(key)
        counted.append(ev)
        if ev["type"] in DONE_TYPES:
            done[ev["id"]] = ev

    base_xp = sum(ev["xp"] for ev in counted)

    completed = []  # [{"module", "ts", "bonus"}] in completion-ts order
    for mod in curriculum.get("modules", []):
        exercises = mod.get("exercises", [])
        if not exercises:
            continue
        if all(ex["id"] in done for ex in exercises):
            ts = max(done[ex["id"]]["ts"] for ex in exercises)
            bonus = 0
            if not mod.get("no_bonus"):
                bonus = round_to_5(0.4 * sum(ex["xp"] for ex in exercises))
            completed.append({"module": mod["id"], "ts": ts, "bonus": bonus})
    completed.sort(key=lambda c: c["ts"])

    xp = base_xp + sum(c["bonus"] for c in completed)
    level = level_for(xp)

    active_days = sorted({ev["ts"][:10] for ev in counted})

    return {
        "events": events,
        "counted": counted,
        "done": done,
        "xp": xp,
        "base_xp": base_xp,
        "completed": completed,
        "completed_modules": [c["module"] for c in completed],
        "level": level,
        "xp_into_level": xp - level["threshold"],
        "xp_for_next": level["next_threshold"] - level["threshold"],
        "devices": sorted({ev["device"] for ev in events}),
        "active_days": active_days,
    }
