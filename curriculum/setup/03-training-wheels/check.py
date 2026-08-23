import json


def check(ctx):
    marker = ctx.root / ".codin" / "last_sync.json"
    ctx.require(
        marker.exists(),
        "no sync has run on this machine yet.\n"
        "Run: python3 codin.py sync")
    try:
        json.loads(marker.read_text(encoding="utf-8"))
    except ValueError:
        ctx.fail("the sync marker looks damaged - run sync once more.")

    dirty = ctx.run(
        ["git", "status", "--porcelain", "--", "docs/data/events.jsonl"],
        cwd=ctx.root)
    ctx.require(
        not dirty.stdout.strip(),
        "there are progress events newer than your last sync.\n"
        "Run sync once more so everything is safely on GitHub.")

    return ("Sync, demystified: 15 lines you have now seen with your "
            "own eyes. Your dashboard renders whatever the log says.")
