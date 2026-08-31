WORDS = [
    "the shell reads what you type",
    "a kernel is not a shell",
    "pipes connect small tools",
    "the shell expands globs before commands run",
    "permissions decide who may run what",
    "every process has a parent",
    "your shell is just a program",
]
LOGS = ["monday.log", "tuesday.log", "friday.log"]
EXPECTED_COUNT = sum(1 for w in WORDS if "shell" in w)


def setup(ctx):
    bench = ctx.box / "workbench"
    bench.mkdir()
    for name in LOGS:
        (bench / name).write_text("log entry\n" * 3)
    (bench / "words.txt").write_text("\n".join(WORDS) + "\n")
    (bench / "greet.sh").write_text('#!/bin/sh\necho "gate open"\n')
    (bench / "README.txt").write_text("gate p1 workbench\n")
    ctx.run(["git", "init", "-q", "-b", "main"], cwd=bench)
    ctx.run(["git", "config", "user.name", "Codin Learner"], cwd=bench)
    ctx.run(["git", "config", "user.email", "learner@codin.local"], cwd=bench)
    ctx.run(["git", "add", "-A"], cwd=bench)
    ctx.run(["git", "commit", "-qm", "clutter, as found"], cwd=bench)


def check(ctx):
    bench = ctx.box / "workbench"
    ctx.require(bench.is_dir(), "the workbench is missing - "
                "python3 codin.py reset gate-p1 deals a fresh board.")

    stray = [n for n in LOGS if (bench / n).exists()]
    moved = [n for n in LOGS if (bench / "logs" / n).exists()]
    ctx.require(
        not stray and len(moved) == len(LOGS),
        "task 1: expected every .log file inside workbench/logs/ "
        "and none left at the top. (mkdir, then mv with a glob.)")

    count_file = bench / "count.txt"
    ctx.require(count_file.exists(),
                "task 2: no count.txt yet. grep and wc -l are friends "
                "(or grep alone has a counting flag).")
    got = count_file.read_text(encoding="utf-8").strip()
    ctx.require(
        got == str(EXPECTED_COUNT),
        "task 2: count.txt says %r, but that's not how many lines of "
        "words.txt contain 'shell'. Look at the lines, not the words." % got)

    greeting = bench / "greeting.txt"
    ctx.require(
        (bench / "greet.sh").stat().st_mode & 0o100,
        "task 3: greet.sh isn't executable yet (chmod).")
    ctx.require(
        greeting.exists() and "gate open" in greeting.read_text(encoding="utf-8"),
        "task 3: run ./greet.sh and send its output into greeting.txt.")

    log = ctx.git("log", "--format=%s", cwd=bench)
    ctx.require(
        any("gate p1" in line for line in log.splitlines()),
        "task 4: no commit mentioning 'gate p1' yet.")
    status = ctx.git("status", "--porcelain", cwd=bench)
    ctx.require(
        not status.strip(),
        "task 4: the working tree isn't clean - something is still "
        "unstaged or uncommitted (git status shows what).")

    return ("Gate open. Phase 2 - Python - is unlocked, and your "
            "hands did all of it from memory.")
