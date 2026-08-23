"""codin doctor - environment self-test.

Run it on every new machine. All green means every exercise on the
current phase can actually run here.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

from . import state


def _git_config(repo_root, key):
    r = subprocess.run(
        ["git", "-C", str(repo_root), "config", key],
        capture_output=True, text=True, timeout=10,
    )
    return r.stdout.strip()


def checks(repo_root, need_cc=False):
    """-> list of (ok, label, advice-if-not-ok)."""
    out = []

    ok = sys.version_info >= (3, 9)
    out.append((ok, "Python %d.%d" % sys.version_info[:2],
                "install Python 3.9 or newer"))

    ok = shutil.which("git") is not None
    out.append((ok, "git installed",
                "install git (Termux: pkg install git)"))

    name = _git_config(repo_root, "user.name")
    email = _git_config(repo_root, "user.email")
    out.append((bool(name and email), "git identity (%s)" % (name or "unset"),
                'run: git config --global user.name "Your Name" && '
                'git config --global user.email "you@example.com"'))

    remote = _git_config(repo_root, "remote.origin.url")
    out.append((bool(remote), "origin remote", "clone this repo from GitHub "
                "rather than copying the folder"))

    if state.is_termux():
        bad = "/storage/" in str(Path(repo_root).resolve())
        out.append((not bad, "repo lives in Termux home",
                    "move it: shared storage (~/storage) breaks permissions "
                    "and git. Clone into ~ instead."))

    device = state.device_name(repo_root)
    out.append((bool(device), "device named (%s)" % (device or "not yet"),
                "run: python3 codin.py doctor --device desktop   "
                "(or phone, or any name you like)"))

    if need_cc:
        ok = shutil.which("cc") or shutil.which("clang") or shutil.which("gcc")
        out.append((bool(ok), "C compiler",
                    "install one (Termux: pkg install clang; "
                    "Debian/Ubuntu: sudo apt install build-essential)"))
    return out


def set_device(repo_root, name):
    """Name this device and record the label in the committed profile."""
    state.set_device_name(repo_root, name)
    prof_path = Path(repo_root) / "docs" / "data" / "profile.json"
    try:
        prof = json.loads(prof_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        prof = {}
    devices = prof.setdefault("devices", [])
    if name not in devices:
        devices.append(name)
        prof_path.parent.mkdir(parents=True, exist_ok=True)
        prof_path.write_text(json.dumps(prof, indent=1) + "\n", encoding="utf-8")
