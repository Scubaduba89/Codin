# The Roadmap

The whole map, honestly labeled. Everything below already exists as a
folder in `curriculum/` — built modules have exercises; fogged ones are
a `module.json` + README waiting for their phase. Content is authored
just-in-time at each phase boundary, in a short session with the tutor,
progressively more by you (that ramp is deliberate — by M5 you author
alone).

Legend: ✅ built now · 🌫 fogged (arrives at its phase) · ✦ elective
(never gates anything) · 🏔 summit

## Phase 0 — Bootstrap ✅
`setup` — Wired Up · First Commit · Training Wheels · Meet Your Tutor ·
Second Machine (phone). Ends at Level 2 with the full loop running.

## Phase 1 — Terminal & Git survival (≈3–5 weeks) ✅
- `terminal-a1` The Terminal Is a Place ✅
- `terminal-a2` Files & Folders ✅
- `git-b1` The Daily Loop ✅
- `terminal-a3` Permissions ✅
- `terminal-a4` Pipes & Text Streams ✅ (the log boss — you'll meet it
  again in Python and in C)
- **Gate p1** ✅ — cold 10-minute drill; opens Phase 2

## Phase 2 — Python core + shell depth (≈6–10 weeks)
- `python-c1` Back in the Saddle ✅ (refresher)
- `python-c2` 🌫 Collections & Loops (the log boss, in Python)
- `terminal-a5` 🌫 Environment & PATH
- `python-c3` 🌫 Functions & Structure ("make the committed tests pass")
- `web-d1` 🌫 Read Your Own Dashboard
- `python-c4` 🌫 Files, JSON & Errors (read the platform's brain)
- `terminal-a6` 🌫 Processes & Jobs (the OS drip-feed begins)
- `git-b2` 🌫 Branching & Merging (one scripted conflict, on purpose)
- `python-c5` 🌫 Stdlib Superpowers (ship the flashcards CLI)
- `terminal-a7` 🌫 Shell Scripting
- `workshop-m1` 🌫 Your First Platform Feature (branch → PR → merged)
- **Gate p2** 🌫 — a 15-line JSON-reading script, cold

## Phase 3 — Data & Web (≈5–8 weeks)
- `data-e1` 🌫 Tables & Queries → `data-e2` 🌫 Modeling & JOINs →
  `data-e3` 🌫 SQL from Python → `data-e4` 🌫 Aggregation (on your own
  progress data)
- `web-d2` 🌫 CSS (restyle your dashboard) → `web-d3` 🌫 JS →
  `web-d4` 🌫 Fetch & Render → `web-d5` 🌫 Stats Page & the SVG Tree
  (the tree rewrite is deliberately yours)
- `git-b3` 🌫 History & Repair (bisect a planted bug; tag v1.0)
- `python-c6` 🌫 Objects & Testing (debugging dojo)
- `terminal-a8` 🌫 The Toolbelt (bin/ project)
- `workshop-m2` 🌫 The Great Migration (progress cache → SQLite) ·
  `workshop-m3` 🌫 Quiz Mode, Yours · `workshop-m4` 🌫 Write a Badge
  Rule (it awards retroactively)
- **Gate p3** 🌫 — one JOIN + render one list, cold

## Phase 4 — C & the machine (≈8–12 weeks)
- `c-f1` 🌫 Hello, Compiler → `c-f2` 🌫 The Stack → `c-f3` 🌫 Pointers &
  Memory (smallest steps; segfaults are specimens) → `c-f4` 🌫 Structs
  → `c-f5` 🌫 Syscalls (strace) → `c-f6` 🌫 fork/exec/wait
- `machine-g1` 🌫 What a Kernel Is → `g2` 🌫 /proc → `g3` 🌫 Memory →
  `g4` 🌫 Filesystems → `g5` 🌫 How Programs Become Processes
- 🏔 `c-f7` 🌫 **Write Your Own Shell** — five staged milestones, ending
  with your shell running `git commit` on this repo (SHELLWRIGHT)
- **Gate p4** 🌫 — explain everything between typing `ls` and seeing
  output (oral exam with the tutor)

## Phase 5 — Consolidation & the homelab bridge (ongoing)
- `machine-gp` 🌫 The Explainer ("How Linux works, as far as I can
  tell" — published with your own strace captures)
- `workshop-m5` 🌫 Author an Exercise · `workshop-m6` 🌫✦ Own Your
  Pipeline
- `machine-g6` 🌫✦ Deeper Water — mini-ps in C, a TCP echo server,
  namespaces; signposts to OSTEP, xv6, Linux From Scratch (someday
  summits, named so they stop being mythical)
- 🏔 `homelab-h1` 🌫 **Self-Hosted** — this dashboard, on your own
  server, on your own network. The hand-off to the homelab journey.

## What never changes

XP only for verified doing · the repo is the single source of truth ·
no loss mechanics · everything runs the same on desktop and Termux ·
the platform stays small enough to read end-to-end, because owning it
is the curriculum.
