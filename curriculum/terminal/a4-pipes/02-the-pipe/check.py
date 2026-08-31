GUESTS = ("ada", "linus", "grace", "dennis", "margaret", "ken")
GUEST_LINES = 137
LETTERS = 23


def setup(ctx):
    with (ctx.box / "guestbook.txt").open("w") as f:
        for i in range(GUEST_LINES):
            f.write("entry %03d: %s was here\n"
                    % (i + 1, GUESTS[i % len(GUESTS)]))
    letters = ctx.box / "letters"
    letters.mkdir()
    for i in range(LETTERS):
        (letters / ("letter-%02d.txt" % (i + 1))).write_text(
            "Dear keeper of the lighthouse, (no. %d)\n" % (i + 1))


def _number_in(ctx, rel, hint):
    raw = ctx.read(rel).strip()
    ctx.require(
        raw.split() and raw.split()[0].isdigit(),
        "%s doesn't start with a number yet. %s" % (rel, hint))
    ctx.require(
        len(raw.split()) == 1,
        "%s holds more than a bare number - looks like wc was handed "
        "a filename. Feed it through the pipe instead: when wc reads "
        "from `|` it has no name to print." % rel)
    return int(raw)


def check(ctx):
    ctx.require(
        ctx.exists("line-count.txt"),
        "no `line-count.txt` yet. Pipe the guestbook through the "
        "counter: cat guestbook.txt | wc -l > line-count.txt")
    n = _number_in(
        ctx, "line-count.txt",
        "Aim the pipeline's output at it with `>` (step 2).")
    ctx.require(
        n == GUEST_LINES,
        "line-count.txt holds %d, but the guestbook has a different "
        "number of lines. Re-run the pipeline from step 2 exactly." % n)
    ctx.require(
        ctx.exists("letter-count.txt"),
        "guestbook counted. Now the letters: ls letters | wc -l, "
        "aimed at letter-count.txt (step 3).")
    m = _number_in(
        ctx, "letter-count.txt",
        "ls prints one name per line - pipe that into wc -l (step 3).")
    ctx.require(
        m == LETTERS,
        "letter-count.txt holds %d, but that's not how many files "
        "sit in letters/. Count with ls letters | wc -l - and make "
        "sure you're listing the letters folder, not the sandbox." % m)
    return ("Two counts, zero files opened. The pipe is yours now - "
            "everything downstream of this is plumbing.")
