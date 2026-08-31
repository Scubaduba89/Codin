JUNK = ["build.log", "debug.log", "scratch.tmp"]


def setup(ctx):
    shop = ctx.box / "workshop"
    shop.mkdir()
    ctx.run(["git", "init", "-q", "-b", "main"], cwd=shop)
    ctx.run(["git", "config", "user.name", "Codin Learner"], cwd=shop)
    ctx.run(["git", "config", "user.email", "learner@codin.local"], cwd=shop)
    (shop / "project.txt").write_text("the actual work\n")
    ctx.run(["git", "add", "-A"], cwd=shop)
    ctx.run(["git", "commit", "-qm", "the project"], cwd=shop)
    for name in JUNK:
        (shop / name).write_text("machine noise\n")


def check(ctx):
    shop = ctx.box / "workshop"
    ctx.require(shop.is_dir(), "the workshop is missing - "
                "python3 codin.py reset git-b1-03 for a fresh one.")

    missing = [n for n in JUNK if not (shop / n).exists()]
    ctx.require(
        not missing,
        "the junk files were deleted (%s) - the lesson is to IGNORE "
        "them, not remove them. Reset and try with .gitignore."
        % ", ".join(missing))
    ctx.require(
        (shop / ".gitignore").exists(),
        "no .gitignore yet - a file with that exact name (leading "
        "dot), one glob pattern per line.")
    status = ctx.git("status", "--porcelain", cwd=shop)
    ctx.require(
        not status.strip(),
        "git status still reports something:\n%s\n"
        "Either a pattern doesn't cover it, or .gitignore itself "
        "isn't committed yet." % status)
    tracked = ctx.git("ls-tree", "--name-only", "HEAD", cwd=shop)
    ctx.require(
        ".gitignore" in tracked,
        "the ignore list works but isn't committed - it's part of "
        "the project's rules, so it belongs in history.")

    return ("Noise silenced, permanently and on purpose. Every status "
            "from here on is signal.")
