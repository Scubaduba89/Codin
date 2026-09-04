"""codin sync - training wheels for the daily git loop.

This really is the whole trick: commit the progress log if it changed,
pull --rebase, push. Read it; by Git module B1 you'll be typing these
commands yourself.

Every failure path here says two things out loud: what git said, and
whether your progress reached GitHub. A sync that half-worked must
never read like one that worked.
"""

import json
import subprocess
from datetime import datetime, timezone

from . import events, state

DASHBOARD_URL = "https://scubaduba89.github.io/Codin/"


def _git(repo_root, *args, check=False):
    return subprocess.run(
        ["git", "-C", str(repo_root)] + list(args),
        capture_output=True, text=True, timeout=120, check=check,
    )


def _event_count(repo_root):
    return len(events.load(repo_root)[0])


def _said(proc):
    """git's own words. A killed or silent process still gets a message."""
    text = (proc.stderr or "").strip() or (proc.stdout or "").strip()
    if not text:
        return "git exited with code %d and said nothing." % proc.returncode
    return text


def _mark(repo_root, pulled, pushed):
    """Record that a sync was attempted, and whether it reached GitHub."""
    marker = state.dir_(repo_root) / "last_sync.json"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text(json.dumps({
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pulled": max(pulled, 0),
        "pushed": bool(pushed),
    }) + "\n", encoding="utf-8")


def run(repo_root):
    """-> human-readable report lines. Commits log changes, pulls, pushes."""
    before = _event_count(repo_root)
    lines = []
    pulled = 0

    dirty = _git(repo_root, "status", "--porcelain", "--",
                 "docs/data/events.jsonl")
    if dirty.stdout.strip():
        _git(repo_root, "add", "docs/data/events.jsonl")
        # the pathspec keeps anything else you have staged out of this commit
        commit = _git(repo_root, "commit", "-m", "progress: sync events",
                      "--", "docs/data/events.jsonl")
        if commit.returncode != 0:
            _mark(repo_root, 0, False)
            return lines + [
                "could not commit your progress - git said:\n" + _said(commit),
                "Your XP is safe in docs/data/events.jsonl, but it is NOT on "
                "GitHub yet.",
            ]
        lines.append("committed your new progress events")

    pull = _git(repo_root, "pull", "--rebase")
    if pull.returncode != 0:
        _mark(repo_root, 0, False)
        return lines + [
            "pull failed - git said:\n" + _said(pull),
            "Nothing was published - your progress is NOT on GitHub yet, "
            "only on this machine.",
        ]
    pulled = _event_count(repo_root) - before
    if pulled > 0:
        lines.append("pulled %d event%s from another device"
                     % (pulled, "s" if pulled != 1 else ""))

    push = _git(repo_root, "push")
    if push.returncode != 0:
        _mark(repo_root, pulled, False)
        return lines + [
            "push failed - git said:\n" + _said(push),
            "Your progress is committed on this machine but NOT on GitHub "
            "yet. Read git's message above - it usually names the fix.",
        ]

    _mark(repo_root, pulled, True)
    lines.append("pushed - GitHub has your progress now")
    lines.append("the dashboard catches up within ~10 minutes: " + DASHBOARD_URL)
    return lines


def unsynced_count(repo_root):
    """How many earned events are not on GitHub yet.

    Counts uncommitted AND committed-but-unpushed lines. With no upstream
    at all, nothing can have been published, so the whole log counts. This
    never answers 0 for a state it cannot read - a silent 0 would tell the
    learner their work is safe when it isn't.
    """
    try:
        upstream = _git(repo_root, "rev-parse", "--abbrev-ref", "@{upstream}")
        if upstream.returncode != 0:
            return _event_count(repo_root)
        diff = _git(repo_root, "diff", "@{upstream}", "--",
                    "docs/data/events.jsonl")
        if diff.returncode != 0:
            return _event_count(repo_root)
        return sum(1 for line in diff.stdout.splitlines()
                   if line.startswith("+{"))
    except Exception:
        return _event_count(repo_root)


def nudge_lines(repo_root, py="python3 codin.py"):
    """What to say after XP is earned, so a win is never silently local."""
    n = unsynced_count(repo_root)
    if not n:
        return []
    if n == 1:
        return [
            "This win is on this machine only. The dashboard shows what has",
            "reached GitHub - publish it with:  %s sync" % py,
        ]
    return ["%d wins are not on GitHub yet - publish them:  %s sync" % (n, py)]
