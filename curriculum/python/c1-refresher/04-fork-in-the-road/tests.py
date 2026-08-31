"""Checks for python-c1-04. Committed and read-only: the checker runs
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

classify = getattr(solution, "classify", None)
if not callable(classify):
    bail("solution.py needs a function named classify.\n"
         "It starts like: def classify(n):")

CASES = [(-100, "negative"), (-1, "negative"), (0, "zero"),
         (1, "small"), (5, "small"), (9, "small"),
         (10, "big"), (11, "big"), (1000, "big")]
HINTS = {
    -1: "anything below 0 is negative",
    0: "zero is its own category - `==` asks, `=` assigns",
    1: "1 is the first small number",
    9: "9 is the last small number",
    10: "10 is the first big one - is that comparison < or <=?",
}

for n, want in CASES:
    try:
        with redirect_stdout(io.StringIO()):
            got = classify(n)
    except Exception as e:
        bail("classify(%d) crashed with %s: %s" % (n, type(e).__name__, e))
    if got != want:
        hint = HINTS.get(n)
        bail("classify(%d) returned %r, expected %r.%s"
             % (n, got, want, "\n(%s)" % hint if hint else ""))
print("ok")
