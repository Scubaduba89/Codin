TARGETS = {
    "secrets.txt": (0o666, 0o640, "launch codes: butter croissant\n"),
    "deploy.sh": (0o600, 0o755, "#!/bin/sh\necho \"deploying nothing, safely\"\n"),
}


def setup(ctx):
    for name, (start, _, body) in TARGETS.items():
        p = ctx.box / name
        p.write_text(body)
        p.chmod(start)


def check(ctx):
    for name, (_, want, _) in TARGETS.items():
        ctx.require(
            ctx.exists(name),
            "`%s` is missing. Fresh copies:\n"
            "python3 codin.py reset terminal-a3-03" % name)
        got = ctx.mode_bits(name)
        ctx.require(
            got == want,
            "%s is mode %03o, but the brief asks for exactly %03o.\n"
            "Price the trios again (r=4 w=2 x=1) and chmod once more."
            % (name, got, want))
    return "640, 755 - you speak permissions in numbers now."
