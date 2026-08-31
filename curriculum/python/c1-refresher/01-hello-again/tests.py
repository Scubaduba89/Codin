"""Checks for python-c1-01. Committed and read-only: the checker runs
this against the solution.py in your sandbox. Reading it is allowed."""
import io
import os
import subprocess
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.getcwd())


def bail(msg):
    print(msg)
    raise SystemExit(1)


with redirect_stdout(io.StringIO()):
    import solution

name = getattr(solution, "NAME", None)
if name is None:
    bail("solution.py defines no NAME yet.\n"
         "Add a line near the top: NAME = \"...\" with a name inside.")
if not isinstance(name, str):
    bail("NAME is a %s, but it should be a string - text in quotes."
         % type(name).__name__)
if not name.strip():
    bail("NAME is an empty string. Put an actual name in the quotes.")

r = subprocess.run([sys.executable, "solution.py"],
                   capture_output=True, text=True, timeout=10)
if r.returncode != 0:
    bail("`python3 solution.py` crashed:\n"
         + "\n".join(r.stderr.strip().splitlines()[-3:])
         + "\n(run it yourself and read the message bottom-up)")
lines = [l for l in r.stdout.splitlines() if l.strip()]
if len(lines) != 1:
    bail("running solution.py should print exactly one line; "
         "yours printed %d." % len(lines))
expected = "Hello, %s!" % name
if lines[0] != expected:
    bail("it printed   %r\nexpected     %r\n"
         "(capital H, a comma, one space, `!` at the end - and the\n"
         "name must come from the NAME variable)" % (lines[0], expected))

src = open("solution.py", encoding="utf-8").read()
if 'f"' not in src and "f'" not in src:
    bail("the output is right, but build the line with an f-string -\n"
         "an f before the opening quote, the variable in {braces} -\n"
         "rather than gluing pieces by hand. That's the habit this\n"
         "exercise is here to restore.")
print("ok")
