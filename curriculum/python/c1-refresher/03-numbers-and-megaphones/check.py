# python-c1-03: two small functions, edges included. tests.py judges.


def check(ctx):
    ctx.require(
        ctx.exists("solution.py"),
        "no `solution.py` in your sandbox yet - it defines area and\n"
        "shout, specs in the instructions.")
    ctx.run_python_tests()
    return ("Two clean functions and you poked the edges yourself - "
            "that's real programming hygiene.")
