"""Checks for python-c1-03. Committed and read-only: the checker runs
this against the solution.py in your sandbox. Reading it is allowed."""
import io
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.getcwd())


def bail(msg):
    print(msg)
    raise SystemExit(1)


with redirect_stdout(io.StringIO()):
    import solution

for fname in ("area", "shout"):
    if not callable(getattr(solution, fname, None)):
        bail("solution.py needs a function named %s - both functions\n"
             "live in this one file." % fname)


def call(label, fn, *args):
    try:
        with redirect_stdout(io.StringIO()):
            return fn(*args)
    except Exception as e:
        bail("%s crashed with %s: %s" % (label, type(e).__name__, e))


for args, want in [((3, 4), 12), ((2.5, 4), 10.0), ((0, 7), 0),
                   ((10, 10), 100)]:
    got = call("area(%r, %r)" % args, solution.area, *args)
    if got != want:
        bail("area(%r, %r) returned %r, expected %r.\n"
             "Width times height, RETURNED (not printed)."
             % (args[0], args[1], got, want))

for text, want in [("ship it", "SHIP IT!"), ("hi", "HI!"),
                   ("OK", "OK!"), ("", "!")]:
    got = call("shout(%r)" % text, solution.shout, text)
    if got != want:
        edge = ""
        if text == "":
            edge = "\n(the empty string still earns its `!`)"
        elif text == "OK":
            edge = "\n(already-loud text gets exactly one `!`)"
        bail("shout(%r) returned %r, expected %r.%s\n"
             "ALL CAPS via .upper(), then one `!` glued on the end."
             % (text, got, want, edge))
print("ok")
