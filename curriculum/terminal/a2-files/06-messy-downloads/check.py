KINDS = ("images", "pdfs", "text", "archives")
FILES = {
    "IMG_20250104_133702.jpg": "images",
    "IMG_20250104_133705.jpg": "images",
    "photo-final-FINAL2.jpg": "images",
    "Screenshot from 2025-11-02 09-41.png": "images",
    "wallpaper(1).png": "images",
    "bank-statement-2025-08.pdf": "pdfs",
    "Boarding Pass LHR.pdf": "pdfs",
    "scan0001.pdf": "pdfs",
    "taxes_FINAL_v3 (2).pdf": "pdfs",
    "notes.txt": "text",
    "todo(old).txt": "text",
    "random thoughts.txt": "text",
    "wifi-password.txt": "text",
    "project-backup.tar.gz": "archives",
    "dotfiles.tar.gz": "archives",
    "fonts.zip": "archives",
    "Old Photos.zip": "archives",
    "sample_data.zip": "archives",
}


def body_of(name):
    return "[%s] pretend contents, faithfully preserved\n" % name


def setup(ctx):
    dl = ctx.box / "downloads"
    dl.mkdir()
    for name in FILES:
        (dl / name).write_text(body_of(name))


def check(ctx):
    dl = ctx.box / "downloads"
    ctx.require(
        dl.is_dir(),
        "the downloads folder itself is gone - deal a fresh mess: "
        "python3 codin.py reset terminal-a2-06")
    for kind in KINDS:
        ctx.require(
            (dl / kind).is_dir(),
            "no `downloads/%s` folder yet - build the four homes "
            "first, inside downloads." % kind)
    for name, kind in sorted(FILES.items()):
        target = dl / kind / name
        if target.is_file():
            ctx.require(
                target.read_text(encoding="utf-8") == body_of(name),
                "`%s` reached %s/ but its contents changed - a moved "
                "file keeps its bytes exactly.\nFresh mess: "
                "python3 codin.py reset terminal-a2-06" % (name, kind))
            continue
        hits = [p for p in dl.rglob("*") if p.is_file() and p.name == name]
        ctx.require(
            hits,
            "`%s` has vanished entirely - deleted instead of moved?\n"
            "Deal a fresh mess: python3 codin.py reset terminal-a2-06"
            % name)
        where = str(hits[0].parent.relative_to(dl))
        if where == ".":
            ctx.fail(
                "`%s` is still loose at the top of downloads - it "
                "belongs in %s/. A glob will carry it, awkward name "
                "and all." % (name, kind))
        ctx.fail(
            "`%s` ended up in downloads/%s - it belongs in %s/. "
            "mv it again; moving twice is free." % (name, where, kind))
    loose = sorted(p.name for p in dl.iterdir() if p.is_file())
    if loose:
        ctx.fail(
            "every file reached a home, but the top of downloads "
            "still has loose copies (`%s`%s) - mv empties the "
            "hallway; rm any strays a cp left behind." % (
                loose[0], ", ..." if len(loose) > 1 else ""))
    return ("Eighteen strays, four homes, an empty hallway. This "
            "exact ritual - mkdir the homes, then mv *.kind - will "
            "tame every real Downloads folder you ever meet. Boss "
            "down; the quiz awaits: python3 codin.py quiz terminal-a2")
