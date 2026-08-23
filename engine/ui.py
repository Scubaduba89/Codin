"""Terminal rendering: colors, bars, and brief celebrations.

Celebrations are deliberately short - peak, then hand control back.
"""

import os
import sys

_COLORS = {
    "green": "32", "yellow": "33", "blue": "34", "magenta": "35",
    "cyan": "36", "dim": "2", "bold": "1", "red": "31",
}


def _want_color():
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def c(text, *names):
    if not _want_color():
        return text
    codes = ";".join(_COLORS[n] for n in names)
    return "\x1b[%sm%s\x1b[0m" % (codes, text)


def bar(cur, total, width=24):
    total = max(total, 1)
    filled = int(width * min(cur, total) / total)
    return c("█" * filled, "green") + c("░" * (width - filled), "dim")


def say(text=""):
    print(text)


def headline(text):
    print()
    print(c(text, "bold"))


def win(xp, exercise_title):
    print()
    print(c("  ✔ PASS", "green", "bold") + "  %s" % exercise_title)
    print(c("  +%d XP" % xp, "yellow", "bold"))


def level_up(level):
    print()
    print(c("  ★ LEVEL %d — %s ★" % (level["number"], level["name"]), "magenta", "bold"))


def badge(b):
    print()
    print(c("  %s Badge earned: %s" % (b.get("icon", "◆"), b["name"]), "cyan", "bold"))
    print(c("    %s" % b.get("desc", ""), "dim"))


def fail(message):
    print()
    print(c("  ✘ Not yet.", "yellow", "bold"))
    for line in message.splitlines():
        print("  " + line)
    print(c("  (No XP lost - nothing is ever lost here. Adjust and re-run check.)", "dim"))


def date_short(ts):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return "%s %d" % (months[int(ts[5:7]) - 1], int(ts[8:10]))
