# python-c1-02: functions that RETURN. tests.py is the judge; its
# output becomes the learner's diagnostic.


def check(ctx):
    ctx.require(
        ctx.exists("solution.py"),
        "no `solution.py` in your sandbox yet - it holds one small\n"
        "function. The instructions have the exact shape.")
    ctx.run_python_tests()
    return ("greet hands its value back instead of shouting it - "
            "that's the move most functions make.")
