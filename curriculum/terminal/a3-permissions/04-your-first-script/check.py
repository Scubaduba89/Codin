LINES = ("made by hand", "run by the kernel")
SCRIPT = "mine.sh"

# No setup(): this one starts from a truly empty sandbox. The learner
# authors every byte.


def check(ctx):
    ctx.require(
        ctx.exists(SCRIPT),
        "no `%s` in the sandbox yet. Open the editor and write it:\n"
        "nano %s" % (SCRIPT, SCRIPT))
    body = ctx.read(SCRIPT)
    first = body.splitlines()[0] if body.splitlines() else ""
    ctx.require(
        first.startswith("#!"),
        "%s exists, but its FIRST line isn't a shebang. The kernel "
        "looks at the first two bytes - make them `#!`, followed by "
        "the interpreter's path." % SCRIPT)
    ctx.require(
        "sh" in first,
        "the shebang doesn't name a shell. This script speaks shell, "
        "so point the kernel at one (step 2 shows the classic).")
    ctx.require(
        ctx.is_executable(SCRIPT),
        "%s has its shebang but no `x` bit - the kernel never even "
        "gets asked. One chmod stands between you and a working "
        "program." % SCRIPT)
    r = ctx.run(["./" + SCRIPT])
    ctx.require(
        r.returncode == 0,
        "./%s starts but exits with an error:\n%s\nRead it, fix the "
        "script, run again." % (SCRIPT, (r.stderr.strip() or "(no output)")))
    missing = [l for l in LINES if l not in r.stdout]
    if missing:
        ctx.fail(
            "the script runs, but its output is missing the line "
            "\"%s\" - check your echo lines against step 2." % missing[0])
    ctx.require(
        ctx.exists("proof.txt"),
        "it runs. Last move: capture a run into proof.txt with `>`.")
    proof = ctx.read("proof.txt")
    ctx.require(
        all(l in proof for l in LINES),
        "proof.txt doesn't hold the script's output yet. Run "
        "./%s again and aim it at proof.txt with `>`." % SCRIPT)
    return ("You wrote a program and the kernel ran it off your shebang. "
            "Take the quiz: python3 codin.py quiz terminal-a3")
