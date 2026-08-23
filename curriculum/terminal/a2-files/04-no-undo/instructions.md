`rm` removes files. Say it plainly: there is no trash can and no
undo. What rm takes stays taken. That's exactly why we practice it
here, where a fresh board is always one command away.

Your sandbox is a writing desk. Keep the work, clear the clutter:

    KEEP    novel.txt, research/
    DELETE  novel.txt.tmp, crash.log, junk-drawer/

1. Look before you delete - always:

       ls

2. Remove the two clutter files (rm takes several names at once):

       rm novel.txt.tmp crash.log

3. Now `rm junk-drawer`. It refuses - like cp, plain rm won't
   touch directories. Read the complaint, then mean it:

       rm -r junk-drawer

   `-r` takes the folder and everything inside. Respect it.

4. `ls` once more. Novel and research still on the desk? Good eye.
5. `python3 codin.py check terminal-a2-04`

If you ever delete the wrong thing IN HERE, no drama:
`python3 codin.py reset terminal-a2-04` always deals a new board.
Out in the world there is no reset - so build the habit now: ls
first, read the name twice, then Enter.
