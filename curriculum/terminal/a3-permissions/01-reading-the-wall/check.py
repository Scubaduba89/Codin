import re

FILES = {
    "diary.txt": (0o600, "owner's eyes only\n"),
    "bulletin.txt": (0o644, "public notice: soup at noon\n"),
    "launch.sh": (0o755, "#!/bin/sh\necho \"liftoff\"\n"),
}
EXPECTED = [
    ("diary", "answer 1 isn't right yet. You want the file whose "
     "group and others trios are ALL dashes - nobody but the owner "
     "gets even an r."),
    ("launch", "answer 2 isn't right yet. Runnable means an `x` "
     "somewhere in the trios - scan ls -l for it."),
    ("no", "answer 3 isn't right yet. Look at bulletin.txt's LAST "
     "trio (others): is there a `w` in it?"),
]


def setup(ctx):
    for name, (mode, body) in FILES.items():
        p = ctx.box / name
        p.write_text(body)
        p.chmod(mode)


def _norm(line):
    line = line.strip().lower()
    line = re.sub(r"^(line\s*)?[123][.):]\s*", "", line)
    return re.sub(r"\.(txt|sh)$", "", line)


def check(ctx):
    for name, (mode, _) in FILES.items():
        if not ctx.exists(name) or ctx.mode_bits(name) != mode:
            ctx.fail("the three files were rearranged, so the "
                     "questions no longer match. Fresh board:\n"
                     "python3 codin.py reset terminal-a3-01")
    ctx.require(
        ctx.exists("answers.txt"),
        "no `answers.txt` in the sandbox yet.\n"
        "Run `ls -l`, read the trios, then echo your three answers "
        "in (one per line).")
    lines = [l for l in ctx.read("answers.txt").splitlines() if l.strip()]
    ctx.require(
        len(lines) == 3,
        "answers.txt has %d non-empty line(s); the format is exactly "
        "three - filename, filename, yes-or-no." % len(lines))
    for got, (want, nudge) in zip(map(_norm, lines), EXPECTED):
        ctx.require(got == want, nudge)
    return "You can read a file's rulebook at a glance now."
