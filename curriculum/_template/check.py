# Exercise checker template. Contract:
#   setup(ctx)  - optional; builds the sandbox (files, practice repos)
#   check(ctx)  - required; verifies OBSERVABLE STATE and either
#                 returns a one-line pass message or raises via
#                 ctx.require/ctx.fail with a friendly diagnostic that
#                 names what was expected - never the answer.
# ctx helpers live in engine/checkers.py (read it - it's short).


def setup(ctx):
    (ctx.box / "starting-point.txt").write_text("as found\n")


def check(ctx):
    ctx.require(
        ctx.exists("result.txt"),
        "expected `result.txt` in the sandbox - the instructions' "
        "step 2 creates it.")
    return "A sentence of earned meaning goes here."
