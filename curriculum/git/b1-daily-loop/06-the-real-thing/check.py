def check(ctx):
    note = ctx.root / "notes" / "daily-loop.md"
    ctx.require(
        note.exists(),
        "no notes/daily-loop.md in the repo yet.\n"
        "mkdir -p notes, then write your cheatsheet with nano.")
    body = note.read_text(encoding="utf-8").strip()
    lines = [l for l in body.splitlines() if l.strip()]
    ctx.require(
        len(body) >= 60 and len(lines) >= 3,
        "the cheatsheet is pretty bare - give future-you at least a "
        "few real lines (what status, add, commit, pull and push "
        "each mean to you).")

    tracked = ctx.run(
        ["git", "ls-tree", "--name-only", "HEAD", "notes/daily-loop.md"],
        cwd=ctx.root)
    ctx.require(
        "daily-loop.md" in tracked.stdout,
        "the file exists but isn't committed - add it, commit it.")

    dirty = ctx.run(
        ["git", "status", "--porcelain", "--", "notes/"], cwd=ctx.root)
    ctx.require(
        not dirty.stdout.strip(),
        "notes/ still has uncommitted changes - finish the loop.")

    upstream = ctx.run(["git", "rev-parse", "@{upstream}"], cwd=ctx.root)
    ctx.require(
        upstream.returncode == 0,
        "this branch has no upstream - `git push` wires it up.")
    unpushed = ctx.run(
        ["git", "rev-list", "@{upstream}..HEAD", "--count", "--",
         "notes/daily-loop.md"], cwd=ctx.root)
    ctx.require(
        unpushed.stdout.strip() == "0",
        "committed - but the cheatsheet isn't on GitHub yet. git push")

    return ("That's a real commit on the real internet, in your own "
            "words. The daily loop is yours now - Daily Driver.")
