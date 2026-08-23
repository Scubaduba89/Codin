Type `*` and the shell expands it, before the command even runs,
into every name that matches. `*.txt` means "every name ending in
.txt". One pattern can stand for a whole crowd of files.

Your sandbox's top level: four `.txt` notes, three `.log` files,
one `README.md`. Empty `notes/` and `audit/` folders stand ready.

1. See what a pattern matches BEFORE acting on it - the safe habit:

       ls *.txt

2. Move all the notes at once:

       mv *.txt notes/

3. Copy - not move! - all the logs into the audit folder:

       cp *.log audit/

4. Survey with `ls`: the .txt files are gone from the top, the
   .log files are still here (copies travel, originals stay), and
   README.md never matched either pattern, so it never moved.

5. `python3 codin.py check terminal-a2-05`

Seven files handled in two commands, no names typed. Step 1 is the
professional reflex: ls the glob first - especially, later in
life, before handing a glob to rm.
