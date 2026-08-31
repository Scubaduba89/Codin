def check(ctx):
    from engine import events, state

    device = state.device_name(ctx.root)
    ctx.require(
        device,
        "name this machine first: python3 codin.py doctor --device phone")

    evs, _ = events.load(ctx.root)
    others = {ev["device"] for ev in evs} - {device}
    ctx.require(
        evs,
        "the event log here is empty - run `python3 codin.py sync` to "
        "pull your history from GitHub first.")
    ctx.require(
        others,
        "this log only knows the device '%s'.\n"
        "Run this check from your SECOND machine (after doctor --device "
        "and sync there) - the point is proving your progress travels."
        % device)

    return ("Two machines, one story. Anywhere you can open a terminal "
            "is now a place you can learn.")
