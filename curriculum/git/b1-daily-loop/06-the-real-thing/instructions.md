No sandbox this time. This one happens in the real repo, lands on the
real GitHub, and stays in your history forever - because you're ready.

1. From the repo root, make yourself a notes folder and write your
   own daily-loop cheatsheet - YOUR words, not copied phrasing.
   A few lines about what each move means to you now:

       mkdir -p notes
       nano notes/daily-loop.md

   (Something like: what status tells you, what add chooses, what a
   commit is, when to pull and push. If you can explain it in your
   own words, you own it.)

2. Walk your cheatsheet through the full loop, for real:

       git status
       git add notes/daily-loop.md
       git commit -m "my daily loop cheatsheet"
       git push

   (You may see `docs/data/events.jsonl` modified in status too -
   that's your recent XP waiting for a sync. Leave it; it isn't part
   of this commit's one idea.)

3. `python3 codin.py check git-b1-06`

Open github.com/Scubaduba89/Codin afterwards and look at your file
sitting in the cloud. This module started with toy repos; it ends
with you shipping. That was not practice.
