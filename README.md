# Codin

A personal, self-paced platform for learning to code — built for one
learner, living entirely in this repo. Real exercises run in a real
terminal, every verified win earns XP, and a static dashboard renders
the sum of all the work visibly coming together.

**The dashboard:** once GitHub Pages is enabled (see below), it lives at
`https://scubaduba89.github.io/Codin/` and updates within ~10 minutes
of any push. Locally it's always instant: `cd docs && python3 -m
http.server 8321`, then open http://localhost:8321 (any free port
works - handy when a homelab already squats on the common ones).

## The idea in five lines

1. You do real things in a real terminal; `python3 codin.py check`
   verifies the result and pays XP. Nothing else ever does.
2. Progress is an append-only log (`docs/data/events.jsonl`), committed
   to git — syncing your progress *is* daily git practice.
3. The dashboard is static files reading that log. Levels, badges, and
   the skill tree are recomputed from history every time, never stored.
4. Claude Code acts as a tutor inside this repo (`claude`, then
   `/lesson`) — it guides, it never solves.
5. Extending this platform is itself part of the curriculum (the
   Workshop track). By Phase 3 you'll be running on code you improved.

## Install (desktop Linux — 5 commands)

```
git clone https://github.com/Scubaduba89/Codin ~/codin
cd ~/codin
python3 codin.py doctor
python3 codin.py doctor --device desktop
python3 codin.py check setup-01
```

That last command is your first win. From then on, one command always
knows the way: `python3 codin.py next` — and `python3 codin.py` alone
shows where you stand.

## Phone (Android · Termux)

Exercise `setup-05` walks you through it, any time during Phase 1.
Short version: install **Termux from F-Droid** (not the Play Store —
that build is abandoned), then:

```
pkg install python git gh
gh auth login
cd ~ && git clone https://github.com/Scubaduba89/Codin codin
cd codin
python3 codin.py doctor --device phone
python3 codin.py sync
```

**The phone guarantee:** `python3 codin.py next --phone --minutes 15`
(the `--phone` is automatic on Termux) always offers something
completable — a due review or a phone-tagged micro-exercise. No honest
15-minute phone session ends at zero XP.

## How progress works (the honest mechanics)

- Every verified pass appends one line to `docs/data/events.jsonl`.
  Only the CLI writes it. XP, levels, badges, module bonuses — all
  recomputed from that log by two engines (Python CLI, dashboard JS)
  that implement one spec (`SPEC.md`) and pass one shared test fixture.
- Two devices append freely; `.gitattributes` union-merge means their
  histories weave without conflicts. Passing the same exercise twice
  (or on both devices) is a no-op, never a farm.
- **No loss mechanics.** No streaks to break, no decay, no red. A
  7-day gap earns you a *Comeback* badge on return, not a guilt trip.
- Gates (`codin gate p1`) are cold self-tests that open the next
  phase. Free retakes forever.

## The tutor

Open `claude` in the repo. `/lesson` teaches what's next, `/hint`
climbs a four-rung ladder that never reaches "the answer", `/check`
interprets results, `/review` is a friendly oral exam after projects,
`/stuck` shrinks the task when it's too much.

`.claude/settings.json` hard-denies the tutor write-access to the two
things that must never be touched: the event log (your progress) and
`.codin/` runtime state. Checkers, tests, and quiz banks are guarded
by a strict written rule instead — hard-blocking them proved to also
block the sanctioned workflow where you and the tutor co-author new
modules at each phase boundary. Full enforcement of "no AI solutions"
is impossible for a self-directed adult anyway — you could always ask
another AI — so the design goal is honest friction on the anti-cheat
core plus an always-on tutor persona that holds the line *with* you.
This repo trains the skill you can't delegate; that's its whole point.

## One-time repo setup (after merging to the default branch)

GitHub → repo **Settings → Pages → Source: Deploy from a branch →
Branch: main, folder `/docs`** → Save. A couple of minutes later the
dashboard is live at `https://scubaduba89.github.io/Codin/`.
(`docs/test.html` on the live site double-checks the JS engine against
the shared fixture in your actual browser.)

## FAQ

**Termux says "Process completed (signal 9)".** Android kills
background phone processes aggressively ("phantom process killing").
It can hit long-running commands. Just re-run; for chronic cases,
plug the phone in and disable battery optimization for Termux.

**Why must the repo live in `~` on Termux, not `~/storage`?** Shared
storage doesn't support Unix permissions or symlinks — git and the
permissions exercises both break there. `codin doctor` warns if the
repo is in the wrong place.

**The public dashboard is behind my local one.** GitHub Pages caches
for ~10 minutes after a push. Every page shows "progress as of …" so
you always know which snapshot you're seeing. The local preview
(`python3 -m http.server 8321` in `docs/`) is always current.

**`git push` asks for a password.** Use `gh auth login` once per
machine (HTTPS + browser login); it configures git credentials for
GitHub.

**I broke a sandbox.** `python3 codin.py reset <exercise-id>` deals a
fresh one. The event log is never touched — nothing is ever lost.

**Where's my data?** All of it is in this repo, in plain text you can
read: `docs/data/events.jsonl` (progress), `quizzes/` (question
banks), `SPEC.md` (the math). There is no server, no account, no
telemetry — just git.

## Layout

```
codin.py          the CLI (python3 codin.py --help)
engine/           the whole engine — stdlib only, small on purpose
SPEC.md           the engine contract both implementations obey
curriculum/       modules and exercises (folders = the skill tree)
quizzes/          question banks (answers stored as hashes)
projects/  bin/   things you build; your toolbelt
docs/             the dashboard (GitHub Pages serves this folder)
tests/            engine tests + the shared conformance fixture
.claude/          tutor persona, skills, and guardrails
ROADMAP.md        every phase and module, including the fog
```
