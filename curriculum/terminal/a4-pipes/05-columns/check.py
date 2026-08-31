CREW = (
    ("zora", "captain", "lisbon"),
    ("ines", "navigator", "porto"),
    ("kofi", "cook", "accra"),
    ("mira", "engineer", "split"),
    ("tavi", "lookout", "nadi"),
    ("odell", "surgeon", "cork"),
    ("suki", "quartermaster", "osaka"),
    ("brin", "carpenter", "bergen"),
)


def setup(ctx):
    (ctx.box / "crew.txt").write_text(
        "\n".join(":".join(row) for row in CREW) + "\n")


def _column(ctx, rel, want, label, flag_hint):
    lines = [l.strip() for l in ctx.read(rel).splitlines() if l.strip()]
    roles = [row[1] for row in CREW]
    if lines == roles:
        ctx.fail(
            "%s holds the crew's ROLES - that's field 2. You want "
            "%s: count the colons again and adjust -f." % (rel, label))
    ctx.require(
        lines == list(want),
        "%s should hold exactly the %s, one per line, roster order.\n"
        "The slice you want: %s" % (rel, label, flag_hint))


def check(ctx):
    ctx.require(
        ctx.exists("names.txt"),
        "no `names.txt` yet. Slice field 1 out of the roster with "
        "cut (step 1) and aim it there with `>`.")
    _column(ctx, "names.txt", [r[0] for r in CREW], "names",
            "delimiter colon, field one")
    ctx.require(
        ctx.exists("ports.txt"),
        "names sliced. Now the home ports - same cut, different "
        "field number (step 2).")
    _column(ctx, "ports.txt", [r[2] for r in CREW], "home ports",
            "delimiter colon, field three")
    return ("cut -d -f: columns fall out of any colon-riddled file. "
            "/etc/passwd will never look like noise again.")
