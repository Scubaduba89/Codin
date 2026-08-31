The `>` you've been using has a sibling: `>>`. Both send a command's
output into a file instead of onto the screen - but they treat what's
already IN the file very differently. `>` wipes the file first
(old-timers call this CLOBBERING). `>>` adds to the end.

You'll keep a tiny ship's journal, one day per line.

1. Day one - create the journal:

       echo "day 1: left the harbor" > journal.txt

2. Days two and three - append, don't clobber:

       echo "day 2: open sea" >> journal.txt
       echo "day 3: dolphins" >> journal.txt

   `cat journal.txt` should now show all three days, in order.
   That's a file built in layers.

3. Now watch `>` destroy. Write a draft, then "save over" it with
   a single arrow again:

       echo "first draft" > draft.txt
       echo "final draft" > draft.txt

   `cat draft.txt` - the first draft is simply gone. No warning,
   no undo. One arrow replaces; two arrows extend.

4. Verify:

       python3 codin.py check terminal-a4-01

If the journal came out wrong, no ceremony: run step 1 again to
clobber it and rebuild. Sometimes the wipe is exactly what you want.
