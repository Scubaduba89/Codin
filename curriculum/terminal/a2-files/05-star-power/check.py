NOTES = {
    "monday.txt": "stand-up at nine, allegedly\n",
    "tuesday.txt": "buy oat milk; learn globs\n",
    "wednesday.txt": "the plants look thirsty\n",
    "ideas.txt": "an app, but for naps\n",
}
LOGS = {
    "build.log": "build ok in 3.2s\n",
    "error.log": "warning: too many warnings\n",
    "install.log": "installed 14 things, needed 2\n",
}
README = "# inbox\nDo not sort me.\n"


def setup(ctx):
    for name, body in NOTES.items():
        (ctx.box / name).write_text(body)
    for name, body in LOGS.items():
        (ctx.box / name).write_text(body)
    (ctx.box / "README.md").write_text(README)
    (ctx.box / "notes").mkdir()
    (ctx.box / "audit").mkdir()


def check(ctx):
    for name, body in sorted(NOTES.items()):
        ctx.require(
            not ctx.exists(name),
            "`%s` is still loose at the top - one mv with a pattern "
            "sweeps every note at once." % name)
        moved = ctx.box / "notes" / name
        ctx.require(
            moved.is_file() and moved.read_text(encoding="utf-8") == body,
            "`notes/%s` is missing (or changed) - the notes should "
            "arrive intact in notes/.\n"
            "Fresh board: python3 codin.py reset terminal-a2-05" % name)
    for name, body in sorted(LOGS.items()):
        original = ctx.box / name
        ctx.require(
            original.is_file()
            and original.read_text(encoding="utf-8") == body,
            "`%s` vanished from the top level - the logs were to be "
            "COPIED, and cp leaves originals in place.\n"
            "Fresh board: python3 codin.py reset terminal-a2-05" % name)
        copy = ctx.box / "audit" / name
        ctx.require(
            copy.is_file() and copy.read_text(encoding="utf-8") == body,
            "no copy of `%s` in audit/ yet - cp takes a pattern just "
            "as happily as mv does." % name)
    readme = ctx.box / "README.md"
    ctx.require(
        readme.is_file() and readme.read_text(encoding="utf-8") == README,
        "README.md got swept away - neither pattern should match a "
        ".md file.\nFresh board: python3 codin.py reset terminal-a2-05")
    return ("Seven files, two commands, zero names typed. The star "
            "works for you now.")
