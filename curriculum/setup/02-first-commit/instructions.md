Time for real git - typed by hand, no training wheels. You'll make a
file, then walk it through the four moves of the daily loop.

1. Make the terminal say hello into a file (`>` sends the output into
   a file instead of the screen):

       echo "hello from my desktop" > projects/hello.txt

2. Now ask git what changed:

       git status

   Read what it says. You should see `projects/hello.txt` as new -
   and `docs/data/events.jsonl` as modified. **That file is your
   progress.** Every XP you earn is a line in it, and git is how it
   travels between your machines.

3. Stage and commit your file (a commit is a saved snapshot with your
   name on it):

       git add projects/hello.txt
       git commit -m "my first commit"

4. Send it to GitHub:

       git push

5. Then:

       python3 codin.py check setup-02

If any step complains, read the message slowly - git's messages
usually tell you the exact command to run next. Getting comfortable
with that is the actual exercise.
