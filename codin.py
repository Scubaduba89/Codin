#!/usr/bin/env python3
"""Codin — a personal learning platform that lives in this repo.

Run `python3 codin.py` for your status, `python3 codin.py next` for
exactly one thing to do. Everything is stdlib; everything works the
same on desktop Linux and Termux.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine import cli  # noqa: E402


def build_parser():
    p = argparse.ArgumentParser(
        prog="python3 codin.py",
        description="Your learning platform. No arguments = status.",
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("status", help="level, XP, recent wins, and what's next")

    log = sub.add_parser("log", help="recent progress events")
    log.add_argument("-n", type=int, default=15)

    sub.add_parser("tree", help="the whole map, in the terminal")
    sub.add_parser("badges", help="badge case + what's within reach")
    sub.add_parser("index", help="regenerate docs/data/curriculum.json (content authoring)")
    sub.add_parser("sync", help="pull other devices' progress, push yours")

    doc = sub.add_parser("doctor", help="check this machine is ready")
    doc.add_argument("--device", help="name this device (e.g. desktop, phone)")

    tm = sub.add_parser("tutor-mark")  # used by the Claude tutor skills
    tm.add_argument("name")

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    cmd = args.cmd or "status"
    handler = getattr(cli, "cmd_" + cmd.replace("-", "_"))
    return handler(ROOT, args) or 0


if __name__ == "__main__":
    sys.exit(main())
