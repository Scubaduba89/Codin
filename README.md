# Codin

A personal, self-paced platform for learning to code — built for one
learner, living in one repo. Real exercises run in the terminal, every
verified win earns XP, and a static dashboard shows the sum of all the
work coming together.

> Full install instructions, the Termux (Android) guide, and the FAQ
> land at the bottom of this file. This is a working skeleton while the
> platform is scaffolded; see `ROADMAP.md` for the whole map and
> `SPEC.md` for how the engine works.

## The idea in five lines

1. You do real things in a real terminal; `python3 codin.py check`
   verifies the result and pays XP. Nothing else ever does.
2. Progress is an append-only log, committed to git — syncing your
   progress *is* git practice.
3. A static dashboard (GitHub Pages) renders XP, badges, and a skill
   tree from that log. Nothing is stored twice.
4. Claude Code acts as a tutor inside this repo — it guides, it never
   solves.
5. Extending this platform is itself part of the curriculum.
