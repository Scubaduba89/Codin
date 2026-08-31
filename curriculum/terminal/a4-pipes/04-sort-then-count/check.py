COUNTS = {"apple": 7, "banana": 5, "cherry": 4, "kiwi": 3, "mango": 5}
STRIDE = 11  # coprime with 24 -> a full shuffle, no adjacent twins


def _orders():
    grouped = []
    for fruit in sorted(COUNTS):
        grouped += [fruit] * COUNTS[fruit]
    n = len(grouped)
    return [grouped[(i * STRIDE) % n] for i in range(n)]


def setup(ctx):
    (ctx.box / "orders.txt").write_text("\n".join(_orders()) + "\n")


def check(ctx):
    ctx.require(
        ctx.exists("tally.txt"),
        "no `tally.txt` yet. Build the frequency table (step 3) and "
        "aim it there with `>`.")
    rows = []
    for line in ctx.read("tally.txt").splitlines():
        parts = line.split()
        if not parts:
            continue
        ctx.require(
            len(parts) == 2 and parts[0].isdigit(),
            "each tally line should be a count and a fruit, the way "
            "uniq -c prints them. Rebuild it with step 3's pipeline.")
        rows.append((int(parts[0]), parts[1]))
    expected = [(COUNTS[f], f) for f in sorted(COUNTS)]
    if len(rows) > len(expected):
        ctx.fail(
            "tally.txt lists the same fruit more than once - the "
            "signature of uniq WITHOUT sort. uniq only compares "
            "neighbors; line the twins up first (step 2).")
    ctx.require(
        rows == expected,
        "tally.txt exists, but the counts aren't the true totals of "
        "orders.txt. The pipeline is sort first, uniq -c second - "
        "run step 2 on the screen and watch the difference.")
    return ("sort | uniq -c: any list, instant frequency table. "
            "Shopkeepers and sysadmins run on this one.")
