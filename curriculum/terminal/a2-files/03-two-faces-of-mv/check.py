REPORT = "Quarterly report: everything is fine.\n"
RECEIPT = "One (1) mechanical keyboard. No refunds.\n"


def setup(ctx):
    (ctx.box / "repotr.txt").write_text(REPORT)
    (ctx.box / "receipt.txt").write_text(RECEIPT)
    (ctx.box / "archive").mkdir()


def check(ctx):
    ctx.require(
        not ctx.exists("repotr.txt"),
        "`repotr.txt` is still there, typo and all - "
        "the rename face of mv fixes it in one line.")
    report = ctx.box / "report.txt"
    if not report.is_file():
        if (ctx.box / "archive" / "report.txt").exists() or \
                (ctx.box / "archive" / "repotr.txt").exists():
            ctx.fail(
                "the report wandered into archive/ - only the receipt "
                "gets filed; the report stays at the top level.\n"
                "(mv it back out: mv archive/<name> .)")
        ctx.fail(
            "no `report.txt` at the top level yet - rename the "
            "misspelled file; its contents come along for free.")
    ctx.require(
        report.read_text(encoding="utf-8") == REPORT,
        "report.txt is there, but its words changed - mv renames, it "
        "never rewrites.\n"
        "Fresh board: python3 codin.py reset terminal-a2-03")
    ctx.require(
        not ctx.exists("receipt.txt"),
        "`receipt.txt` is still at the top - the move face: "
        "mv <file> <folder>/")
    filed = ctx.box / "archive" / "receipt.txt"
    ctx.require(
        filed.is_file() and filed.read_text(encoding="utf-8") == RECEIPT,
        "the receipt isn't in archive/ (or isn't intact) - it should "
        "arrive there unchanged.\n"
        "Fresh board: python3 codin.py reset terminal-a2-03")
    return "Rename and move: one command, two faces, zero mystery."
