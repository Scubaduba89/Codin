"""Command implementations behind codin.py.

Each cmd_* takes (repo_root, parsed_args). Heavy lifting lives in the
sibling modules; this file is wiring and words.
"""

import json
from pathlib import Path

from . import (badges, content, doctor as doctor_mod, events, indexer,
               nextup, rules, state as state_mod, sync as sync_mod, ui)

PY = "python3 codin.py"


def load_world(repo_root):
    """-> (curriculum, replay_state, ignored_count)"""
    curriculum = content.load_curriculum(repo_root)
    evs, ignored = events.load(repo_root)
    st = rules.replay(evs, curriculum)
    return curriculum, st, ignored


def due_review_count(repo_root, curriculum, st):
    try:
        from . import review
    except ImportError:
        return 0
    return len(review.due_items(repo_root, curriculum, st))


def _module_progress(mod, st):
    total = len(mod["exercises"])
    done = sum(1 for ex in mod["exercises"] if ex["id"] in st["done"])
    return done, total


def in_progress_modules(curriculum, st, local):
    started_mods = set()
    for ex_id in local.get("started", {}):
        kind, ex = content.find(curriculum, ex_id)
        if kind == "exercise":
            started_mods.add(ex["module"])
    out = []
    for mod in curriculum["modules"]:
        if not mod["exercises"] or mod["id"] in local.get("parked", []):
            continue
        done, total = _module_progress(mod, st)
        if 0 < done < total or (done < total and mod["id"] in started_mods):
            out.append(mod)
    return out


def print_next(repo_root, suggestion):
    ui.headline("Next up")
    if suggestion["kind"] == "exercise":
        ex = suggestion["exercise"]
        ui.say("  [%s] %s — ~%d min (%s)" % (ex["id"], ex["title"], ex["minutes"], suggestion["why"]))
        ui.say("  → %s start %s" % (PY, ex["id"]))
    elif suggestion["kind"] == "review":
        ui.say("  %d review item%s due. (%s)" % (
            suggestion["due"], "s" if suggestion["due"] != 1 else "", suggestion["why"]))
        ui.say("  → %s review" % PY)
    else:
        ui.say("  " + suggestion["why"])


def cmd_status(repo_root, args):
    curriculum, st, ignored = load_world(repo_root)
    local = state_mod.load(repo_root)
    lv = st["level"]
    ui.headline("CODIN — Level %d · %s" % (lv["number"], lv["name"]))
    ui.say("  %s  %d XP · %d to next level" % (
        ui.bar(st["xp_into_level"], st["xp_for_next"]),
        st["xp"], lv["next_threshold"] - st["xp"]))

    mods = in_progress_modules(curriculum, st, local)
    if mods:
        ui.headline("In progress")
        for mod in mods:
            done, total = _module_progress(mod, st)
            ui.say("  %s %s  %s %d/%d" % (
                mod["id"].ljust(14), mod["title"].ljust(28),
                ui.bar(done, total, 10), done, total))

    wins = [ev for ev in st["counted"] if ev["type"] != "review"][-5:]
    if wins:
        ui.headline("Recent wins")
        for ev in reversed(wins):
            ui.say("  %s  %s  +%d XP" % (ui.date_short(ev["ts"]), ev["id"].ljust(18), ev["xp"]))

    due = due_review_count(repo_root, curriculum, st)
    unsynced = sync_mod.unsynced_count(repo_root)
    notes = []
    if due:
        notes.append("%d review%s due (%s review)" % (due, "s" if due != 1 else "", PY))
    if unsynced:
        notes.append("%d event%s not on GitHub yet (%s sync)" % (
            unsynced, "s" if unsynced != 1 else "", PY))
    if ignored:
        notes.append("%d malformed log line%s ignored" % (ignored, "s" if ignored != 1 else ""))
    if notes:
        ui.say("")
        for n in notes:
            ui.say("  · " + n)

    local_state = state_mod.load(repo_root)
    print_next(repo_root, nextup.suggest(
        curriculum, st, local_state,
        phone=state_mod.is_termux(), due_reviews=due))
    ui.say("")


def cmd_log(repo_root, args):
    _, st, _ = load_world(repo_root)
    ui.headline("Recent events")
    for ev in st["events"][-args.n:]:
        ui.say("  %s  %-9s %-24s +%d XP  (%s)" % (
            ev["ts"][:10], ev["type"], ev["id"], ev["xp"], ev["device"]))
    if not st["events"]:
        ui.say("  Nothing yet. Your first win is minutes away: %s check setup-01" % PY)
    ui.say("")


def cmd_tree(repo_root, args):
    curriculum, st, _ = load_world(repo_root)
    local = state_mod.load(repo_root)
    started_mods = {content.find(curriculum, ex_id)[1]["module"]
                    for ex_id in local.get("started", {})
                    if content.find(curriculum, ex_id)[0] == "exercise"}
    tracks = {}
    for mod in curriculum["modules"]:
        tracks.setdefault(mod["track"], []).append(mod)
    ui.headline("The map (✔ done · ◐ in progress · ○ open · ✦ optional · 🔒 locked · ⋯ future)")
    for track in sorted(tracks, key=lambda t: min(m["phase"] for m in tracks[t])):
        ui.say("")
        ui.say("  " + ui.c(track.upper(), "bold"))
        for mod in tracks[track]:
            done, total = _module_progress(mod, st)
            unlocked_mod, unmet = content.requirements_met(curriculum, mod, st)
            if not mod["exercises"]:
                glyph, note = "⋯", ui.c("(future)", "dim")
            elif done == total:
                glyph, note = ui.c("✔", "green"), ""
            elif done > 0 or mod["id"] in started_mods:
                glyph, note = ui.c("◐", "yellow"), "%d/%d" % (done, total)
            elif not unlocked_mod:
                glyph, note = "🔒", ui.c("(unlocks after %s)" % ", ".join(unmet), "dim")
            elif mod.get("elective"):
                glyph, note = ui.c("✦", "cyan"), ui.c("(optional)", "dim")
            else:
                glyph, note = "○", ""
            ui.say("   %s %s %s %s" % (glyph, mod["id"].ljust(14), mod["title"].ljust(34), note))
    ui.say("")


def cmd_badges(repo_root, args):
    curriculum, st, _ = load_world(repo_root)
    defs = badges.load_defs(repo_root)
    earned = badges.evaluate(defs, st)
    ui.headline("Badge case (%d earned)" % len(earned))
    for b in earned:
        ui.say("  %s %-22s %s  %s" % (
            b.get("icon", "◆"), b["name"], ui.date_short(b["earned_ts"]),
            ui.c(b.get("desc", ""), "dim")))
    if not earned:
        ui.say("  Empty - for now. The first one is minutes away.")
    teasers = badges.next_teasers(defs, st)
    if teasers:
        ui.headline("Within reach")
        for b in teasers:
            ui.say("  %s %-22s %s" % (b.get("icon", "◇"), b["name"], ui.c(b["desc"], "dim")))
    ui.say("")


def cmd_index(repo_root, args):
    curriculum, written = indexer.write_index(repo_root)
    n_ex = sum(len(m["exercises"]) for m in curriculum["modules"])
    ui.say("indexed %d modules / %d exercises" % (len(curriculum["modules"]), n_ex))
    for path in written:
        ui.say("  wrote %s" % Path(path).relative_to(repo_root))


def cmd_doctor(repo_root, args):
    if args.device:
        doctor_mod.set_device(repo_root, args.device)
        ui.say("This device is now called %s." % ui.c(args.device, "bold"))
    curriculum, st, _ = load_world(repo_root)
    need_cc = any(
        m["track"] == "c" and m["exercises"] and
        content.requirements_met(curriculum, m, st)[0]
        for m in curriculum["modules"]
    )
    rows = doctor_mod.checks(repo_root, need_cc=need_cc)
    ui.headline("Doctor")
    bad = 0
    for ok, label, advice in rows:
        mark = ui.c("✔", "green") if ok else ui.c("✘", "red")
        ui.say("  %s %s" % (mark, label))
        if not ok:
            bad += 1
            ui.say("     → " + advice)
    ui.say("")
    if bad == 0:
        ui.say(ui.c("  All green.", "green", "bold") +
               " Try: %s check setup-01" % PY)
    else:
        ui.say("  %d thing%s to fix, then run doctor again." % (bad, "s" if bad != 1 else ""))
    ui.say("")
    return 0 if bad == 0 else 1


def cmd_sync(repo_root, args):
    ui.headline("Sync")
    for line in sync_mod.run(repo_root):
        ui.say("  · " + line)
    ui.say(ui.c("  (This command is ~15 lines of Python: engine/sync.py. Worth a read.)", "dim"))
    ui.say("")


def cmd_tutor_mark(repo_root, args):
    allowed = {"lesson", "hint", "check", "review", "stuck"}
    if args.name not in allowed:
        ui.say("unknown marker")
        return 1
    state_mod.mark(repo_root, "tutor-" + args.name)
    return 0
