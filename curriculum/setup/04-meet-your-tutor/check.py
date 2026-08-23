def check(ctx):
    from engine import state

    ctx.require(
        state.has_mark(ctx.root, "tutor-lesson"),
        "the tutor hasn't given you a /lesson on this machine yet.\n"
        "Open Claude Code in this repo and type: /lesson")
    ctx.require(
        state.has_mark(ctx.root, "tutor-hint"),
        "you've had a lesson - now try /hint once, so you know the "
        "shape of the ladder before you need it for real.")

    return ("Introductions made. From here on, the tutor is `claude` "
            "away - and the checker is the only judge of done.")
