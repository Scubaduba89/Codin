JOURNAL = (
    "day 1: left the harbor",
    "day 2: open sea",
    "day 3: dolphins",
)

# No setup(): the learner writes every byte with > and >>.


def check(ctx):
    ctx.require(
        ctx.exists("journal.txt"),
        "no `journal.txt` yet. Day one starts it with a single `>` "
        "(step 1).")
    lines = [l.strip() for l in ctx.read("journal.txt").splitlines()
             if l.strip()]
    ctx.require(
        lines == list(JOURNAL),
        "journal.txt exists, but it doesn't hold days 1-3 in order.\n"
        "Day 1 goes in with `>`, days 2 and 3 with `>>`. If a day "
        "clobbered the rest, rebuild from step 1 - that's the lesson "
        "working.")
    ctx.require(
        ctx.exists("draft.txt"),
        "the journal is perfect. Now the demolition: make draft.txt "
        "twice with `>` (step 3) and see what survives.")
    draft = ctx.read("draft.txt")
    ctx.require(
        "first draft" not in draft,
        "draft.txt still contains the first draft. Write the final "
        "draft with a SINGLE `>` - watch it clobber.")
    ctx.require(
        draft.strip() == "final draft",
        "draft.txt should hold exactly one line: the final draft "
        "(step 3, second command).")
    return ("One arrow replaces, two arrows extend - you'll never "
            "lose a file to `>` by accident again.")
