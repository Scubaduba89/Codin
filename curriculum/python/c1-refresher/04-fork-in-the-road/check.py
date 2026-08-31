# python-c1-04: if/elif/else and boundary thinking. tests.py sweeps
# the boundaries; its output is the diagnostic.


def check(ctx):
    ctx.require(
        ctx.exists("solution.py"),
        "no `solution.py` in your sandbox yet - it holds classify(n),\n"
        "four outcomes, spec in the instructions.")
    ctx.run_python_tests()
    return ("Boundaries checked and held: -1, 0, 1, 9, 10 all land "
            "where they should. That's the hard part of if/elif.")
