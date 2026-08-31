NOVEL = "Chapter One. It was a dark and stormy terminal.\n"
INTERVIEWS = "Q: Why the terminal? A: It's where the verbs live.\n"
CLUTTER = ("novel.txt.tmp", "crash.log", "junk-drawer")


def setup(ctx):
    (ctx.box / "novel.txt").write_text(NOVEL)
    (ctx.box / "research").mkdir()
    (ctx.box / "research" / "interviews.txt").write_text(INTERVIEWS)
    (ctx.box / "novel.txt.tmp").write_text(
        "autosave scratch - safe to delete\n")
    (ctx.box / "crash.log").write_text(
        "segfault at 0x0000 - nobody will ever read this\n")
    drawer = ctx.box / "junk-drawer"
    drawer.mkdir()
    (drawer / "expired-coupons.txt").write_text("50% off, in 2019\n")
    (drawer / "broken-shortcut.desktop").write_text("points nowhere\n")


def check(ctx):
    # Keepers first: deleting the wrong thing is THE lesson here.
    novel = ctx.box / "novel.txt"
    ctx.require(
        novel.is_file() and novel.read_text(encoding="utf-8") == NOVEL,
        "`novel.txt` went with the clutter - out in the world that's "
        "a lost novel.\nIn here: python3 codin.py reset terminal-a2-04 "
        "deals a new board. (This is why we ls before we rm.)")
    notes = ctx.box / "research" / "interviews.txt"
    ctx.require(
        notes.is_file() and notes.read_text(encoding="utf-8") == INTERVIEWS,
        "the `research/` folder (or its notes) got deleted - only "
        "junk-drawer was clutter.\n"
        "Fresh board: python3 codin.py reset terminal-a2-04")
    for name in CLUTTER:
        ctx.require(
            not ctx.exists(name),
            "`%s` is still on the desk - rm clears files; folders "
            "need the recursive flag." % name)
    return ("Clutter gone, novel safe. rm respected, not feared - "
            "that's the professional relationship.")
