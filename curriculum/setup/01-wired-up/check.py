def check(ctx):
    from engine import state

    git_name = ctx.run(["git", "config", "user.name"], cwd=ctx.root)
    ctx.require(
        git_name.returncode == 0 and git_name.stdout.strip(),
        "git doesn't know who you are yet.\n"
        "Run: python3 codin.py doctor   - it shows the exact command.")

    remote = ctx.run(["git", "config", "remote.origin.url"], cwd=ctx.root)
    ctx.require(
        remote.returncode == 0 and remote.stdout.strip(),
        "no `origin` remote - this copy isn't connected to GitHub.\n"
        "Clone the repo from GitHub rather than copying the folder.")

    ctx.require(
        state.device_name(ctx.root),
        "this device has no name yet.\n"
        "Run: python3 codin.py doctor --device desktop   (or any name)")

    return "Your machine is wired up. The bar at the top just moved."
