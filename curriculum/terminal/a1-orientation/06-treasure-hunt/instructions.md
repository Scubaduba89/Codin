Everything from this module, one expedition. Your sandbox is an
island. At its entrance there's a `clue.txt`. Each clue names the next
place - some steps go down, some go back up with `..`, one place is
hiding.

Rules of the island:

- `cat clue.txt` reads a clue. Follow it. There are five.
- Everything you need: cd, ls, ls -a, cat, pwd, Tab, and `..`.
- The final room holds `treasure.txt` with a passphrase inside.

When you have the passphrase, return to the island's entrance (the
sandbox's top folder) and record it:

    echo "the passphrase" > found.txt

Then: `python3 codin.py check terminal-a1-06`

No time limit, no wrong turns that matter. `pwd` when disoriented,
`cd` + Tab to travel. Cartographers draw the map as they go: some
people keep a scrap file of where clues pointed - `nano notes.txt` if
you'd like one; it's yours, the checker doesn't care.
