TOWN = {
    "market/stalls": None,
    "harbor/lighthouse": "chest.txt",
    "harbor/docks": None,
    "library/archives": None,
    "library/reading-room": None,
}


def setup(ctx):
    for rel, chest in TOWN.items():
        room = ctx.box / rel
        room.mkdir(parents=True)
        if chest:
            (room / chest).write_text(
                "You found the chest. Now prove you were here:\n"
                "    pwd > path.txt\n")


def check(ctx):
    room = None
    for candidate in ctx.box.rglob("chest.txt"):
        room = candidate.parent
    ctx.require(
        room is not None,
        "the chest is gone - the sandbox may have been rearranged.\n"
        "Fresh start: python3 codin.py reset terminal-a1-01")
    proof = room / "path.txt"
    ctx.require(
        proof.exists(),
        "no `path.txt` in the room with the chest yet.\n"
        "Stand IN that room (ls shows chest.txt), then: pwd > path.txt")
    from pathlib import Path

    written = proof.read_text(encoding="utf-8").strip()
    ctx.require(
        written and Path(written).resolve() == room.resolve(),
        "path.txt exists, but it doesn't hold that room's path.\n"
        "Run `pwd > path.txt` while standing in the chest room "
        "(pwd with nothing else - let the terminal answer).")
    return "You can navigate. The terminal is a place now."
