SECRET = "lanternfish"


def setup(ctx):
    for room in ("attic", "cellar", "parlor"):
        (ctx.box / room).mkdir()
        (ctx.box / room / "furniture.txt").write_text("just furniture\n")
    (ctx.box / "cellar" / ".whisper").write_text(
        "the secret word is: %s\n" % SECRET)


def check(ctx):
    ctx.require(
        ctx.exists("answer.txt"),
        "no `answer.txt` at the top of the sandbox yet.\n"
        "Found the hidden file? Write its word: echo \"word\" > answer.txt")
    answer = ctx.read("answer.txt").strip().strip('"').lower()
    ctx.require(
        answer == SECRET,
        "answer.txt doesn't hold the secret word yet.\n"
        "One of the three rooms hides a dotfile - `ls -a` in each room, "
        "then `cat` what you find.")
    return "ls -a: nothing on this machine can hide from you now."
