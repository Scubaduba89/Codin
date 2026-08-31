CALM = (
    "calm seas, steady wind",
    "charted two small islands",
    "fresh fish for dinner",
    "read at the bow all evening",
    "patched a sail, sang badly",
    "nothing to report",
    "dolphins raced the hull",
)
BAD_DAYS = {
    4: "ERROR: took on water in the fore hold",
    11: "ERROR: compass spinning like a dancer",
    17: "ERROR: kraken sighted (probably a log)",
    23: "ERROR: biscuits reached weapons-grade",
    29: "ERROR: first mate overboard (recovered)",
    38: "ERROR: sail torn clean through",
    44: "ERROR: rum inventory does not add up",
    52: "ERROR: chart eaten by the ship's goat",
    59: "ERROR: anchor raised itself, allegedly",
}
DAYS = 60


def _log_lines():
    lines = []
    for day in range(1, DAYS + 1):
        if day in BAD_DAYS:
            lines.append("day %02d: %s" % (day, BAD_DAYS[day]))
        else:
            lines.append("day %02d: %s" % (day, CALM[day % len(CALM)]))
    return lines


def setup(ctx):
    (ctx.box / "ship-log.txt").write_text(
        "\n".join(_log_lines()) + "\n")


def _lines_of(ctx, rel):
    return [l.rstrip() for l in ctx.read(rel).splitlines() if l.strip()]


def check(ctx):
    expected_bad = [l for l in _log_lines() if "ERROR" in l]
    expected_calm = [l for l in _log_lines() if "ERROR" not in l]
    ctx.require(
        ctx.exists("trouble.txt"),
        "no `trouble.txt` yet. Fish the ERROR lines out of the log "
        "with grep, and aim them at trouble.txt with `>` (step 2).")
    got_bad = _lines_of(ctx, "trouble.txt")
    ctx.require(
        got_bad == expected_bad,
        "trouble.txt should hold exactly the log's ERROR lines, in "
        "log order - no more, no less. grep is case-sensitive: the "
        "log shouts ERROR in capitals.")
    ctx.require(
        ctx.exists("smooth.txt"),
        "trouble captured. Now invert the net: grep -v gives the "
        "lines WITHOUT the word - into smooth.txt (step 3).")
    got_calm = _lines_of(ctx, "smooth.txt")
    ctx.require(
        got_calm == expected_calm,
        "smooth.txt should hold every line that does NOT contain "
        "ERROR - that's grep with the -v flag, same word.")
    return ("grep and grep -v: the haystack never stood a chance. "
            "This is how real logs are read - by not reading them.")
