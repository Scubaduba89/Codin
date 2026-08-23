def setup(ctx):
    (ctx.box / "bakery" / "oven").mkdir(parents=True)
    (ctx.box / "florist" / "counter").mkdir(parents=True)


def check(ctx):
    note = ctx.box / "florist" / "counter" / "note.txt"
    strays = [p for p in ctx.box.rglob("note.txt") if p != note]
    ctx.require(
        note.exists(),
        "no note at florist/counter yet."
        + ("\n(Found one at `%s` - a mis-thrown path! Count the ..s "
           "again, and rm the stray.)" %
           strays[0].relative_to(ctx.box) if strays else
           "\nStand in bakery/oven and aim with ../../"))
    ctx.require(
        note.read_text(encoding="utf-8").strip(),
        "the note arrived empty - echo something into it.")
    return ("Relative paths land where you aim them. `..` is just "
            "'toward the root, one hop'.")
