import shutil


def setup(ctx):
    bare = ctx.box / "github.git"
    ctx.run(["git", "init", "-q", "--bare", "-b", "main", str(bare)])

    local = ctx.box / "local"
    ctx.run(["git", "clone", "-q", str(bare), str(local)])
    for repo in (local,):
        ctx.run(["git", "config", "user.name", "Codin Learner"], cwd=repo)
        ctx.run(["git", "config", "user.email", "learner@codin.local"], cwd=repo)
    (local / "journal.txt").write_text("day one on two machines\n")
    ctx.run(["git", "add", "-A"], cwd=local)
    ctx.run(["git", "commit", "-qm", "start the journal"], cwd=local)
    ctx.run(["git", "push", "-q", "-u", "origin", "main"], cwd=local)

    # the "other machine": clone, push news, vanish
    courier = ctx.box / "courier"
    ctx.run(["git", "clone", "-q", str(bare), str(courier)])
    ctx.run(["git", "config", "user.name", "Other Machine"], cwd=courier)
    ctx.run(["git", "config", "user.email", "other@codin.local"], cwd=courier)
    (courier / "news.txt").write_text(
        "BREAKING: your other machine has thoughts of its own.\n")
    ctx.run(["git", "add", "-A"], cwd=courier)
    ctx.run(["git", "commit", "-qm", "news from the other machine"], cwd=courier)
    ctx.run(["git", "push", "-q"], cwd=courier)
    shutil.rmtree(courier)


def check(ctx):
    local, bare = ctx.box / "local", ctx.box / "github.git"
    ctx.require(local.is_dir() and bare.is_dir(),
                "the miniature world is missing - "
                "python3 codin.py reset git-b1-05 rebuilds it.")

    ctx.require(
        (local / "news.txt").exists(),
        "local/ still hasn't heard the news - `git pull` inside it "
        "fetches what the remote knows.")
    status = ctx.git("status", "--porcelain", cwd=local)
    ctx.require(
        not status.strip() and (local / "reply.txt").exists(),
        "write reply.txt, then walk it through the loop: add, "
        "commit - the tree should end clean.")
    remote_subjects = ctx.git("log", "--format=%s", "main", cwd=bare)
    ctx.require(
        "news from the other machine" in remote_subjects,
        "the remote's history looks rewritten - reset and try again.")
    ctx.require(
        int(ctx.git("rev-list", "--count", "main", cwd=bare)) >= 3,
        "your reply never reached the remote - committed is not "
        "pushed. One more move: git push")
    local_head = ctx.git("rev-parse", "HEAD", cwd=local)
    remote_head = ctx.git("rev-parse", "main", cwd=bare)
    ctx.require(
        local_head == remote_head,
        "local and remote don't agree yet - push what you committed.")

    return ("Pull, then push: history flowed both ways and nothing "
            "collided. You just did, by hand, what sync does daily.")
