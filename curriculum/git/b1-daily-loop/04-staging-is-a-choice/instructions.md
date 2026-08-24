Why does git make you `add` before you `commit`? Because a commit
should be ONE idea - and your working folder usually holds several at
once. The staging area is where you choose.

Your sandbox's `letters/` repo has two letters, both edited, both
unfinished business. They deserve separate commits.

1. `cd letters`, `git status` - two modified files.

2. Stage and commit ONLY the letter to Alice (name the file, not `.`):

       git add to-alice.txt
       git commit -m "finish the letter to alice"

   Run `git status`: Bob's letter is still waiting, untouched by
   that commit. That's the point.

3. Now Bob's, in its own commit:

       git add to-bob.txt
       git commit -m "finish the letter to bob"

4. Read what you made:

       git log --oneline

   Two commits, one idea each. When you're hunting a bug in month
   six, `git log` reading like a sentence-by-sentence story is what
   saves you.

5. `python3 codin.py check git-b1-04`

`git add .` is for when everything pending IS one idea. Naming files
is for when it isn't. Now you have both moves.
