`wc -l` counts lines. Mildly useful on its own. The magic is the
character `|`, the PIPE: it takes whatever the command on its left
prints and feeds it straight into the command on its right, as
input. Two small tools snap together into a bigger one. That is the
whole Unix philosophy in a single keystroke.

Your sandbox has a `guestbook.txt` far too long to count by eye,
and a `letters/` folder stuffed with files.

1. Look at the problem (don't count - just feel the dread):

       cat guestbook.txt
       ls letters

2. Count the guestbook by piping cat's output into wc:

       cat guestbook.txt | wc -l

   Notice the answer is a bare number. wc read from the pipe, so
   it never learned any filename to print alongside. Save it:

       cat guestbook.txt | wc -l > line-count.txt

3. Now count FILES the same way. `ls letters` prints one name per
   line, and wc doesn't care where lines come from - names, days,
   log entries, it's all just lines to a pipe:

       ls letters | wc -l > letter-count.txt

4. Verify:

       python3 codin.py check terminal-a4-02

You just measured two things without opening a single file. From
here on, most of what you build in the terminal will be plumbing.
