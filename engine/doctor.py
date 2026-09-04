"""codin doctor - environment self-test.

Run it on every new machine. All green means every exercise on the
current phase can actually run here.
"""

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

    if remote:
        # A dry-run push changes nothing on GitHub but proves the whole
        # publish path works. setup-02 needs a real push minutes from now -
        # better to find out here than mid-exercise.
        try:
            probe = subprocess.run(
                ["git", "-C", str(repo_root), "push", "--dry-run", "--quiet"],
                capture_output=True, text=True, timeout=60)
            said = (probe.stderr or "").strip().splitlines()
            out.append((probe.returncode == 0, "can publish to GitHub",
                        "GitHub is not accepting a push from this machine yet.\n"
                        "     Sign in once:  gh auth login   "
                        "(Termux: pkg install gh)\n"
                        "     git said: " + (said[0] if said else "nothing")))
        except subprocess.TimeoutExpired:
            out.append((False, "can publish to GitHub",
                        "GitHub did not answer in 60s - check your connection, "
                        "then run doctor again."))

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
    """Name this device (local state only - the dashboard learns device
    names from the event log, so nothing committed changes here)."""
    state.set_device_name(repo_root, name)
