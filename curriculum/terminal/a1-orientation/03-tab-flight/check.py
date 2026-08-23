CHAIN = ("expedition-supply-depot-alpha/"
         "northern-ridge-approach-route/"
         "glacier-traverse-section-seven/"
         "high-altitude-acclimatization-camp/"
         "basecamp")


def setup(ctx):
    (ctx.box / CHAIN).mkdir(parents=True)
    (ctx.box / CHAIN / "summit-log.txt").write_text(
        "You made it. Plant the flag: touch made-it.txt\n")


def check(ctx):
    flag = ctx.box / CHAIN / "made-it.txt"
    ctx.require(
        flag.exists(),
        "no flag at basecamp yet.\n"
        "Tab your way to the bottom of the expedition chain, then: "
        "touch made-it.txt")
    return "Tab is a reflex now. Your fingers just got years back."
