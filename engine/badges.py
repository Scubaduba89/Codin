"""Badge evaluation. Mirrors SPEC.md §3; docs/js/badges.js is the twin.

Badges are derived, never stored: definitions live in
docs/data/badges.json, and adding a rule there awards it retroactively
from history. Unknown rule kinds are ignored (forward compatibility -
inventing a new kind is Workshop milestone M4 territory).
"""

import json
from pathlib import Path

from . import rules


def load_defs(repo_root):
    path = Path(repo_root) / "docs" / "data" / "badges.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _module_completion_ts(state):
    return {c["module"]: c["ts"] for c in state["completed"]}


def _earned_ts(rule, state):
    """-> the ts the rule fired at, or None if it hasn't. SPEC §3.1."""
    kind = rule.get("kind")
    events, done = state["events"], state["done"]

    if kind == "first_event":
        for ev in state["counted"]:
            if ev["type"] == "pass":
                return ev["ts"]
        return None

    if kind == "exercise":
        ev = done.get(rule.get("id"))
        return ev["ts"] if ev else None

    if kind == "exercises_all":
        ids = rule.get("ids", [])
        if ids and all(i in done for i in ids):
            return max(done[i]["ts"] for i in ids)
        return None

    if kind == "modules_all":
        by_mod = _module_completion_ts(state)
        ids = rule.get("ids", [])
        if ids and all(i in by_mod for i in ids):
            return max(by_mod[i] for i in ids)
        return None

    if kind == "devices":
        need = rule.get("count", 2)
        seen = set()
        for ev in events:
            seen.add(ev["device"])
            if len(seen) >= need:
                return ev["ts"]
        return None

    if kind == "gap_return":
        gap = rule.get("days", 7) * 86400
        prev = None
        for ev in events:
            t = _epoch(ev["ts"])
            if prev is not None and t - prev >= gap:
                return ev["ts"]
            prev = t if prev is None else max(prev, t)
        return None

    return None  # unknown kind: never fires


def _epoch(ts):
    """Seconds since epoch for a SPEC ts (UTC, seconds precision)."""
    from datetime import datetime, timezone

    return int(
        datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )


def evaluate(defs, state):
    """-> earned badges [{key,name,tier,icon,desc,earned_ts}] by earn time."""
    earned = []
    for b in defs:
        ts = _earned_ts(b.get("rule", {}), state)
        if ts is not None:
            row = dict(b)
            row.pop("rule", None)
            row["earned_ts"] = ts
            earned.append(row)
    earned.sort(key=lambda b: b["earned_ts"])
    return earned


def evaluate_all(repo_root, state):
    return evaluate(load_defs(repo_root), state)


def next_teasers(defs, state, limit=3):
    """Up to `limit` not-yet-earned badges worth showing, in file order.

    File order in badges.json is authored roughly by reachability, so
    the first unearned entries are the honest 'next achievable' set.
    """
    earned_keys = {b["key"] for b in evaluate(defs, state)}
    out = []
    for b in defs:
        if b["key"] in earned_keys:
            continue
        out.append({k: b[k] for k in ("key", "name", "tier", "icon", "desc") if k in b})
        if len(out) >= limit:
            break
    return out
