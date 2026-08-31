"""Local runtime state under .codin/ - per-device, never committed.

Holds only conveniences (device name, started/parked bookkeeping,
tutor markers, sync marker). Losing this directory never loses
progress: progress lives in the event log.
"""

import json
import os
from pathlib import Path


def dir_(repo_root):
    return Path(repo_root) / ".codin"


def _file(repo_root):
    return dir_(repo_root) / "state.json"


def load(repo_root):
    path = _file(repo_root)
    if not path.exists():
        return {"started": {}, "parked": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return {"started": {}, "parked": []}


def save(repo_root, state):
    d = dir_(repo_root)
    d.mkdir(exist_ok=True)
    _file(repo_root).write_text(
        json.dumps(state, indent=1) + "\n", encoding="utf-8"
    )


def device_name(repo_root):
    path = dir_(repo_root) / "device.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("name")
    except ValueError:
        return None


def set_device_name(repo_root, name):
    d = dir_(repo_root)
    d.mkdir(exist_ok=True)
    (d / "device.json").write_text(
        json.dumps({"name": name}) + "\n", encoding="utf-8"
    )


def is_termux():
    return "TERMUX_VERSION" in os.environ or "com.termux" in str(Path.home())


def mark(repo_root, name):
    """Drop a named marker file (e.g. tutor-met markers for setup-04)."""
    d = dir_(repo_root) / "markers"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text("ok\n", encoding="utf-8")


def has_mark(repo_root, name):
    return (dir_(repo_root) / "markers" / name).exists()
