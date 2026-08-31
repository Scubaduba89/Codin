IPS = (
    ("203.0.113.42", 41),
    ("198.51.100.7", 29),
    ("192.0.2.146", 23),
    ("203.0.113.9", 17),
    ("198.51.100.23", 13),
    ("192.0.2.201", 11),
    ("203.0.113.77", 9),
    ("198.51.100.180", 7),
)
PATHS = ("/index.html", "/about.html", "/api/status", "/img/logo.png",
         "/contact.html", "/robots.txt", "/blog/post-1.html")
STRIDE = 67  # coprime with 150 -> deterministic full shuffle


def _log_lines():
    grouped = []
    for ip, n in IPS:
        grouped += [ip] * n
    total = len(grouped)
    lines = []
    for k in range(total):
        ip = grouped[(k * STRIDE) % total]
        t = k * 7
        status = 404 if k % 17 == 0 else 200
        size = 512 + (k * 37) % 4096
        lines.append(
            '%s - - [23/Aug/2026:%02d:%02d:%02d +0000] '
            '"GET %s HTTP/1.1" %d %d'
            % (ip, t // 3600, (t // 60) % 60, t % 60,
               PATHS[k % len(PATHS)], status, size))
    return lines


def setup(ctx):
    (ctx.box / "access.log").write_text("\n".join(_log_lines()) + "\n")


def check(ctx):
    ctx.require(
        ctx.exists("access.log"),
        "access.log is missing - the sandbox may have been "
        "rearranged. Fresh start: python3 codin.py reset "
        "terminal-a4-06")
    # Compute the truth from the data itself, same as the learner must.
    counts = {}
    for line in ctx.read("access.log").splitlines():
        if line.strip():
            ip = line.split()[0]
            counts[ip] = counts.get(ip, 0) + 1
    expected = sorted(
        counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    expected = [(n, ip) for ip, n in expected]

    ctx.require(
        ctx.exists("top5.txt"),
        "no `top5.txt` yet. Build the pipeline one stage at a time - "
        "start by slicing the IP column out of access.log with cut.")
    rows = []
    for line in ctx.read("top5.txt").splitlines():
        parts = line.split()  # forgiving about uniq -c's left padding
        if not parts:
            continue
        ctx.require(
            len(parts) == 2 and parts[0].isdigit(),
            "each line of top5.txt should be what uniq -c prints: a "
            "count, then an IP address. Yours has a different shape - "
            "did the cut stage slice out column 1?")
        rows.append((int(parts[0]), parts[1]))
    ctx.require(
        len(rows) == 5,
        "top5.txt holds %d entries - the boss demanded exactly five. "
        "That's head's job, at the very end of the pipe." % len(rows))
    if rows == sorted(expected, key=lambda r: r[1]) or \
            rows == sorted(expected):
        ctx.fail(
            "five entries, right IPs - but not ordered by COUNT, "
            "biggest first. After uniq -c, sort again: numerically "
            "(-n) and reversed (-r).")
    ctx.require(
        rows == expected,
        "top5.txt isn't the true top five yet. Check each stage in "
        "order: cut the first column, sort, uniq -c, sort -rn, "
        "head -5. Run the pipe WITHOUT the final `>` to eyeball it.")
    return ("The Log Boss falls. Remember this one-liner - Python "
            "and C will each take their swing at the same log, and "
            "the Polyglot badge waits past them. Quiz time: python3 "
            "codin.py quiz terminal-a4")
