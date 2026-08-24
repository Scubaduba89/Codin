# python-c1-05: loops, lists, and empty-case thinking. tests.py is
# the judge, empty lists included.


def check(ctx):
    ctx.require(
        ctx.exists("solution.py"),
        "no `solution.py` in your sandbox yet - two functions, one\n"
        "loop pattern each. Specs (empty lists included) are in the\n"
        "instructions.")
    ctx.run_python_tests()
    return ("Loops, lists, ties, and empties - the rust is off. "
            "The module quiz awaits: python3 codin.py quiz python-c1")
