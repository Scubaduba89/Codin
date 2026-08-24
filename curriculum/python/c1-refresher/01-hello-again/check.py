# python-c1-01: variables, print, f-strings.
# The real judge is tests.py (committed next to this file); it runs
# with the learner's sandbox as cwd and its output is the diagnostic.


def check(ctx):
    ctx.require(
        ctx.exists("solution.py"),
        "no `solution.py` in your sandbox yet.\n"
        "cd into the sandbox and create it - the instructions walk "
        "you through the two lines it needs.")
    ctx.run_python_tests()
    return "First program of phase 2: written, run, verified. Welcome back."
