def setup(ctx):
    recipe = ctx.box / "recipe"
    recipe.mkdir()
    ctx.run(["git", "init", "-q", "-b", "main"], cwd=recipe)
    ctx.run(["git", "config", "user.name", "Codin Learner"], cwd=recipe)
    ctx.run(["git", "config", "user.email", "learner@codin.local"], cwd=recipe)
    (recipe / "recipe.txt").write_text(
        "Pan bread\n---------\nflour\nwater\nsalt\n")
    ctx.run(["git", "add", "-A"], cwd=recipe)
    ctx.run(["git", "commit", "-qm", "write down the pan bread recipe"], cwd=recipe)
    (recipe / "recipe.txt").write_text(
        "Pan bread\n---------\nflour\nwater\nsalt\nbutter\n")
    ctx.run(["git", "add", "-A"], cwd=recipe)
    ctx.run(["git", "commit", "-qm", "add the fat"], cwd=recipe)


def check(ctx):
    recipe = ctx.box / "recipe"
    ctx.require(recipe.is_dir(), "the recipe repo is missing - "
                "python3 codin.py reset git-b1-02 for a fresh one.")

    content = (recipe / "recipe.txt").read_text(encoding="utf-8")
    ctx.require(
        "olive oil" in content and "butter" not in content,
        "recipe.txt should call for olive oil now, with butter gone - "
        "edit it with nano, then commit.")
    status = ctx.git("status", "--porcelain", cwd=recipe)
    ctx.require(
        not status.strip(),
        "the change exists but isn't committed yet - the working tree "
        "should end clean (add, then commit).")
    count = int(ctx.git("rev-list", "--count", "HEAD", cwd=recipe))
    ctx.require(count == 3, "the log should hold exactly 3 commits "
                "(two of history plus yours).")
    ctx.require(
        ctx.exists("answer.txt"),
        "one last step: count the commits in `git log --oneline` and "
        "echo the number into answer.txt at the sandbox's top level.")
    ctx.require(
        ctx.read("answer.txt").strip() == "3",
        "answer.txt doesn't match the log - run `git log --oneline` "
        "in recipe/ and count the lines.")

    return ("log is the story, diff is the sentence you're about to "
            "add. You read both before they were permanent.")
