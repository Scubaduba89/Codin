MOOD_FINAL = "hopeful, actually\n"


def setup(ctx):
    diary = ctx.box / "diary"
    diary.mkdir()
    ctx.run(["git", "init", "-q", "-b", "main"], cwd=diary)
    ctx.run(["git", "config", "user.name", "Codin Learner"], cwd=diary)
    ctx.run(["git", "config", "user.email", "learner@codin.local"], cwd=diary)
    (diary / "entry.txt").write_text("Dear diary: started learning git.\n")
    (diary / "mood.txt").write_text("uncertain\n")
    ctx.run(["git", "add", "-A"], cwd=diary)
    ctx.run(["git", "commit", "-qm", "yesterday's entry"], cwd=diary)
    (diary / "mood.txt").write_text(MOOD_FINAL)
    (diary / "gratitude.txt").write_text("tab completion\n")


def check(ctx):
    diary = ctx.box / "diary"
    ctx.require(diary.is_dir(), "the diary is missing - "
                "python3 codin.py reset git-b1-01 for a fresh one.")

    status = ctx.git("status", "--porcelain", cwd=diary)
    ctx.require(
        not status.strip(),
        "git status still shows pending work:\n%s\n"
        "The goal state is a clean working tree - everything staged, "
        "then committed." % status)

    tracked = ctx.git("ls-tree", "--name-only", "HEAD", cwd=diary)
    ctx.require(
        "gratitude.txt" in tracked,
        "gratitude.txt was never committed - untracked files need "
        "`git add` before a commit can include them.")
    shown = ctx.git("show", "HEAD:mood.txt", cwd=diary)
    ctx.require(
        shown.strip() == MOOD_FINAL.strip(),
        "the committed mood.txt is still the old version - the "
        "changed file needed staging too.")
    count = ctx.git("rev-list", "--count", "HEAD", cwd=diary)
    ctx.require(int(count) >= 2, "history looks rewritten - the "
                "original commit should still be there beneath yours.")

    return ("Changed → staged → committed → clean. That's the loop; "
            "everything else in git is a variation on it.")
