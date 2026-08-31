"""Read and append the progress log (docs/data/events.jsonl).

The log is append-only and the single source of truth; see SPEC.md §1.
Only `append()` in this module ever writes to it.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FIELDS = ("v", "uid", "ts", "device", "type", "id", "xp")
EVENT_TYPES = {"pass", "quiz", "review", "gate", "stage", "milestone"}


def log_path(repo_root):
    return Path(repo_root) / "docs" / "data" / "events.jsonl"


def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_uid(etype, eid, ts, device):
    raw = "\n".join([etype, eid, ts, device]).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def parse_lines(lines):
    """Parse raw log lines -> (events, ignored) per SPEC.md §2.1.

    Blank lines are skipped silently; malformed lines are counted but
    never fatal.
    """
    events, ignored = [], 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            ignored += 1
            continue
        if (
            not isinstance(ev, dict)
            or any(field not in ev for field in REQUIRED_FIELDS)
            or ev["type"] not in EVENT_TYPES
            or not isinstance(ev["xp"], int)
            or isinstance(ev["xp"], bool)
        ):
            ignored += 1
            continue
        events.append(ev)
    return events, ignored


def load(repo_root):
    """-> (events in file order, ignored count). Missing file = empty log."""
    path = log_path(repo_root)
    if not path.exists():
        return [], 0
    return parse_lines(path.read_text(encoding="utf-8").splitlines())


def append(repo_root, etype, eid, xp, device, ts=None):
    """Append one event and return it. The only writer of the log."""
    ts = ts or now_ts()
    ev = {
        "v": 1,
        "uid": make_uid(etype, eid, ts, device),
        "ts": ts,
        "device": device,
        "type": etype,
        "id": eid,
        "xp": int(xp),
    }
    path = log_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, separators=(",", ":")) + "\n")
    return ev
