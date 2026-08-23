SPEC_DIRS = ("site", "site/css", "site/img", "site/notes",
             "site/assets", "site/assets/fonts")
SPEC_FILES = ("site/index.html", "site/notes/todo.txt")


def setup(ctx):
    (ctx.box / "blueprint.txt").write_text(
        "BLUEPRINT - build this, exactly:\n"
        "\n"
        "    site/\n"
        "      index.html      (an empty file is fine)\n"
        "      css/\n"
        "      img/\n"
        "      notes/\n"
        "        todo.txt      (empty is fine here too)\n"
        "      assets/\n"
        "        fonts/\n"
        "\n"
        "Tools: mkdir, touch, and mkdir -p for the deep chain.\n")


def check(ctx):
    for rel in SPEC_DIRS:
        p = ctx.box / rel
        if p.is_file():
            ctx.fail(
                "`%s` exists, but as a FILE - the blueprint wants a "
                "folder there.\nRemove it (rm %s), then mkdir it." % (rel, rel))
        ctx.require(
            p.is_dir(),
            "no `%s` directory yet.\n"
            "Check blueprint.txt and mkdir the missing piece "
            "(mkdir -p builds a whole chain)." % rel)
    for rel in SPEC_FILES:
        p = ctx.box / rel
        if p.is_dir():
            ctx.fail(
                "`%s` ended up as a folder - mkdir makes folders, touch "
                "makes files.\nRemove it (rmdir %s), then touch it." % (rel, rel))
        ctx.require(
            p.is_file(),
            "the file `%s` is missing - touch conjures empty files "
            "into being." % rel)
    return ("Built to spec. mkdir and touch: you don't just visit the "
            "filesystem now, you shape it.")
