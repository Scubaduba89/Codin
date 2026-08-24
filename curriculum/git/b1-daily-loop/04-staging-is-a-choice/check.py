def setup(ctx):
    letters = ctx.box / "letters"
    letters.mkdir()
    ctx.run(["git", "init", "-q", "-b", "main"], cwd=letters)
    ctx.run(["git", "config", "user.name", "Codin Learner"], cwd=letters)
    ctx.run(["git", "config", "user.email", "learner@codin.local"], cwd=letters)
    (letters / "to-alice.txt").write_text("Dear Alice,\n")
    (letters / "to-bob.txt").write_text("Dear Bob,\n")
    ctx.run(["git", "add", "-A"], cwd=letters)
    ctx.run(["git", "commit", "-qm", "start both letters"], cwd=letters)
    (letters / "to-alice.txt").write_text(
        "Dear Alice,\nThe terminal is a place now. Visit soon.\n")
    (letters / "to-bob.txt").write_text(
        "Dear Bob,\nI met a shell. It expands globs.\n")


def check(ctx):
    letters = ctx.box / "letters"
    ctx.require(letters.is_dir(), "the letters repo is missing - "
                "python3 codin.py reset git-b1-04 for a fresh one.")

    status = ctx.git("status", "--porcelain", cwd=letters)
    ctx.require(not status.strip(),
                "both letters should end up committed - the tree "
                "isn't clean yet.")
    count = int(ctx.git("rev-list", "--count", "HEAD", cwd=letters))
    ctx.require(
        count == 3,
        "expected exactly 3 commits (the start plus one per letter), "
        "found %d.\nEach letter gets its own commit - stage them BY "
        "NAME, one at a time." % count)
    last_two = []
    for ref in ("HEAD", "HEAD~1"):
        files = ctx.git("show", "--name-only", "--format=", ref,
                        cwd=letters).split()
        last_two.append(sorted(files))
    ctx.require(
        all(len(f) == 1 for f in last_two) and last_two[0] != last_two[1],
        "the two new commits should each touch exactly one letter - "
        "one for Alice, one for Bob.\n(git show --name-only HEAD "
        "shows what a commit touched.)")

    return ("One idea per commit - chosen deliberately, with the "
            "staging area doing exactly the job it exists for.")
