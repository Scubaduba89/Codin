SIZES = {
    "whale.log": 4000,
    "walrus.dat": 900,
    "otter.txt": 220,
    "shrimp.txt": 40,
    "plankton.txt": 3,
}


def setup(ctx):
    for name, size in SIZES.items():
        (ctx.box / name).write_text("x" * size + "\n")


def check(ctx):
    ctx.require(
        ctx.exists("sizes.txt"),
        "no `sizes.txt` yet. Find the sort-by-size flag "
        "(ls --help, or /size inside man ls), then: ls -<flag> > sizes.txt")
    lines = [l.strip() for l in ctx.read("sizes.txt").splitlines() if l.strip()]
    listed = [l for l in lines if l in SIZES]
    expected = sorted(SIZES, key=SIZES.get, reverse=True)
    ctx.require(
        listed == expected,
        "sizes.txt exists, but the files aren't ordered largest-first.\n"
        "You're looking for a single capital-letter ls flag. "
        "The whale should surface on top.")
    return ("--help and man: you now hold the documentation for the "
            "entire operating system.")
