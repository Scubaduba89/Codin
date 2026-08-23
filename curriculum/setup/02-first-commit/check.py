def check(ctx):
    hello = ctx.root / "projects" / "hello.txt"
    ctx.require(
        hello.exists(),
        "expected `projects/hello.txt` to exist.\n"
        'Make it with: echo "hello from my desktop" > projects/hello.txt')
    ctx.require(
        hello.read_text(encoding="utf-8").strip(),
        "projects/hello.txt exists but is empty - give it a greeting.")

    tracked = ctx.run(
        ["git", "ls-tree", "--name-only", "HEAD", "projects/hello.txt"],
        cwd=ctx.root)
    ctx.require(
        "hello.txt" in tracked.stdout,
        "the file exists but isn't committed yet.\n"
        "The moves: git add projects/hello.txt, then git commit -m \"...\"")

    upstream = ctx.run(["git", "rev-parse", "@{upstream}"], cwd=ctx.root)
    ctx.require(
        upstream.returncode == 0,
        "this branch has no upstream on GitHub yet - `git push` should "
        "set it up (git may suggest the exact flag to use).")
    unpushed = ctx.run(
        ["git", "rev-list", "@{upstream}..HEAD", "--count", "--",
         "projects/hello.txt"],
        cwd=ctx.root)
    ctx.require(
        unpushed.stdout.strip() == "0",
        "committed - but not pushed. One more move: git push")

    return ("That commit is on GitHub forever now. You just used the "
            "loop you'll use every day.")
