POEM = "The cursor blinks; the harbor waits.\n"
PHOTOS = {
    "photos/sunrise.jpg": "[imagine a sunrise, 3.1 MB of orange]\n",
    "photos/harbor.jpg": "[imagine a harbor, mostly fog]\n",
    "photos/trip/lighthouse.jpg": "[imagine a lighthouse, slightly tilted]\n",
}
ORIGINALS = dict(PHOTOS)
ORIGINALS["notes/poem.txt"] = POEM


def setup(ctx):
    (ctx.box / "notes").mkdir()
    (ctx.box / "notes" / "poem.txt").write_text(POEM)
    for rel, body in PHOTOS.items():
        p = ctx.box / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    (ctx.box / "backup").mkdir()


def check(ctx):
    # Originals first: cp never eats its source.
    for rel, body in sorted(ORIGINALS.items()):
        p = ctx.box / rel
        ctx.require(
            p.is_file() and p.read_text(encoding="utf-8") == body,
            "the original `%s` is missing or changed - that was a move "
            "(or an edit), not a copy.\ncp leaves sources untouched. "
            "Fresh board: python3 codin.py reset terminal-a2-02" % rel)
    poem_copy = ctx.box / "backup" / "poem.txt"
    ctx.require(
        poem_copy.is_file(),
        "no copy of the poem in `backup/` yet.\n"
        "Aim cp at the file, then at the folder it should land in.")
    ctx.require(
        poem_copy.read_text(encoding="utf-8") == POEM,
        "backup/poem.txt exists but its words differ from the "
        "original - a true copy is identical.\n"
        "Fresh board: python3 codin.py reset terminal-a2-02")
    if not (ctx.box / "backup" / "photos").is_dir():
        if (ctx.box / "backup" / "sunrise.jpg").exists():
            ctx.fail(
                "the photos landed straight in backup/ - copy the "
                "folder ITSELF (aim cp -r at `photos`, not at what's "
                "inside), so it arrives as backup/photos.")
        ctx.fail(
            "no `backup/photos` yet - a whole folder needs cp's "
            "recursive flag. Try plain cp first and read what it says.")
    for rel, body in sorted(PHOTOS.items()):
        copy = ctx.box / "backup" / rel
        ctx.require(
            copy.is_file() and copy.read_text(encoding="utf-8") == body,
            "`backup/%s` is missing - -r should carry everything, "
            "including the trip/ subfolder." % rel)
    return ("Backed up, originals untouched. cp is the 'try it on a "
            "copy' instinct, made real.")
