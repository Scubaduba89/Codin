MAGIC = "the gate swings open"
SCRIPT = "locked.sh"


def setup(ctx):
    p = ctx.box / SCRIPT
    p.write_text("#!/bin/sh\necho \"%s\"\n" % MAGIC)
    p.chmod(0o644)


def check(ctx):
    ctx.require(
        ctx.exists(SCRIPT),
        "`%s` is missing from the sandbox. Fresh copy:\n"
        "python3 codin.py reset terminal-a3-02" % SCRIPT)
    ctx.require(
        ctx.is_executable(SCRIPT),
        "%s still has no `x` for its owner - the shell will keep "
        "refusing. chmod's symbolic dialect adds one right to one "
        "trio." % SCRIPT)
    r = ctx.run(["./" + SCRIPT])
    ctx.require(
        r.returncode == 0 and MAGIC in r.stdout,
        "%s runs, but it no longer prints its original line - the "
        "script itself may have been edited. Reset if needed:\n"
        "python3 codin.py reset terminal-a3-02" % SCRIPT)
    ctx.require(
        ctx.exists("output.txt"),
        "the script runs now, but there's no `output.txt` yet.\n"
        "Run it once more and aim its output at a file with `>`.")
    ctx.require(
        MAGIC in ctx.read("output.txt"),
        "output.txt exists but doesn't hold the script's line. "
        "Capture the real run: ./%s > output.txt" % SCRIPT)
    return "Permission denied, understood and repaired. chmod u+x is yours."
