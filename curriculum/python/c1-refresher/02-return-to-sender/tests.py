"""Checks for python-c1-02. Committed and read-only: the checker runs
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

greet = getattr(solution, "greet", None)
if not callable(greet):
    bail("solution.py needs a function named greet.\n"
         "It starts like: def greet(name):")

for name in ("Ada", "Linus", "Grace Hopper"):
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            got = greet(name)
    except Exception as e:
        bail("greet(%r) crashed with %s: %s\n"
             "(run python3, import it, and try the call yourself)"
             % (name, type(e).__name__, e))
    expected = "Welcome back, %s!" % name
    if got is None and buf.getvalue():
        bail("greet(%r) PRINTED its greeting and returned None.\n"
             "print shows a human; return hands the value back to the\n"
             "caller. Swap the print for a return." % (name,))
    if got is None:
        bail("greet(%r) returned None - it needs a return statement."
             % (name,))
    if not isinstance(got, str):
        bail("greet(%r) returned a %s - it should return a string."
             % (name, type(got).__name__))
    if got != expected:
        bail("greet(%r) returned  %r\n"
             "expected            %r\n"
             "(capital W, the comma, one space, `!` on the end)"
             % (name, got, expected))
print("ok")
