PASSPHRASE = "the map was the territory all along"


def setup(ctx):
    box = ctx.box

    def room(rel):
        p = box / rel
        p.mkdir(parents=True, exist_ok=True)
        return p

    (box / "clue.txt").write_text(
        "Clue 1/5: The journey starts where ships rest - "
        "go into the cove, then the jetty.\n")
    jetty = room("cove/jetty")
    (jetty / "clue.txt").write_text(
        "Clue 2/5: Climb all the way back to the entrance (.. and .. "
        "again), then take the jungle path to the shrine.\n")
    shrine = room("jungle-path/overgrown-steps/shrine")
    (shrine / "clue.txt").write_text(
        "Clue 3/5: A room in this shrine does not appear in plain ls. "
        "Look harder, right here.\n")
    hidden = room("jungle-path/overgrown-steps/shrine/.crypt")
    (hidden / "clue.txt").write_text(
        "Clue 4/5: Step back out to the shrine, then up one, and into "
        "the watchtower beside the steps.\n")
    tower = room("jungle-path/overgrown-steps/watchtower")
    (tower / "clue.txt").write_text(
        "Clue 5/5: From this tower you can see the volcano-observatory-"
        "and-research-outpost at the island's top level. Its vault "
        "holds the treasure. (Tab makes that name painless.)\n")
    vault = room("volcano-observatory-and-research-outpost/vault")
    (vault / "treasure.txt").write_text(
        'The passphrase is exactly:\n\n    %s\n\nCarry it home: at the '
        "sandbox's top folder,\n    echo \"...\" > found.txt\n" % PASSPHRASE)
    for decoy in ("cove/sea-cave", "jungle-path/mudflats"):
        d = room(decoy)
        (d / "note.txt").write_text("Nothing here but weather.\n")


def check(ctx):
    ctx.require(
        ctx.exists("found.txt"),
        "no `found.txt` at the island's entrance yet.\n"
        "The trail starts with: cat clue.txt")
    answer = " ".join(ctx.read("found.txt").strip().strip('"').lower().split())
    ctx.require(
        answer == PASSPHRASE,
        "found.txt doesn't hold the vault's passphrase yet - "
        "check treasure.txt again, and copy the phrase exactly.")
    return ("Five clues, one island, zero fear. Module A1 is in "
            "your hands now - the quiz awaits: python3 codin.py quiz "
            "terminal-a1")
