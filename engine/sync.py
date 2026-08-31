"""codin sync - training wheels for the daily git loop.

This really is the whole trick: commit the progress log if it changed,
pull --rebase, push. Read it; by Git module B1 you'll be typing these
commands yourself.
"""

import json
import subprocess
from datetime import datetime, timezone

from . import events, state


def _git(repo_root, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo_root)] + list(args),
        capture_output=True, text=True, timeout=120, check=check,
    )


def _event_count(repo_root):
    return len(events.load(repo_root)[0])


def run(repo_root):
    """-> human-readable report lines. Commits log changes, pulls, pushes."""
    before = _event_count(repo_root)
    lines = []
    dirty = _git(repo_root, "status", "--porcelain", "--", "docs/data/events.jsonl")
    if dirty.stdout.strip():
        _git(repo_root, "add", "docs/data/events.jsonl")
        _git(repo_root, "commit", "-m", "progress: sync events")
        lines.append("committed your new progress events")
    pull = _git(repo_root, "pull", "--rebase", check=False)
    if pull.returncode != 0:
        return lines + ["pull failed: " + pull.stderr.strip().splitlines()[-1]]
    pulled = _event_count(repo_root) - before
    if pulled > 0:
        lines.append("pulled %d event%s from another device" % (pulled, "s" if pulled != 1 else ""))
    push = _git(repo_root, "push", check=False)
    if push.returncode != 0:
        return lines + ["push failed: " + push.stderr.strip().splitlines()[-1]]
    lines.append("pushed - everything is on GitHub")
    marker = state.dir_(repo_root) / "last_sync.json"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text(json.dumps({
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pulled": max(pulled, 0),
    }) + "\n", encoding="utf-8")
    return lines


def unsynced_count(repo_root):
    """Events not yet safely on the remote (uncommitted + unpushed)."""
    try:
        diff = _git(repo_root, "diff", "@{upstream}", "--",
                    "docs/data/events.jsonl", check=False)
        if diff.returncode != 0:  # no upstream yet
            diff = _git(repo_root, "diff", "HEAD", "--",
                        "docs/data/events.jsonl", check=False)
        return sum(
            1 for line in diff.stdout.splitlines()
            if line.startswith("+{")
        )
    except Exception:
        return 0
