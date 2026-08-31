Some files should never be committed: logs, temp files, caches -
noise that machines regenerate. Your sandbox's `workshop/` repo is
littered with exactly that kind of junk.

1. `cd workshop`, run `git status`, and meet the noise: two `.log`
   files and a `.tmp` file cluttering every status you'll ever run
   here.

2. Git has a permanent answer - a file named `.gitignore` listing
   patterns to stop mentioning. Create it (note the leading dot, and
   remember from A1 how to see dotfiles):

       nano .gitignore

   Two lines inside, using the glob patterns you know from the
   terminal track:

       *.log
       *.tmp

3. Run `git status` again. The junk vanished from the report - though
   `ls` proves the files still exist. Ignored ≠ deleted.

4. The ignore list itself IS worth committing - it's part of the
   project's rules:

       git add .gitignore
       git commit -m "ignore logs and temp files"

5. `python3 codin.py check git-b1-03`

This repo you're learning in has its own `.gitignore` - it's why
`.codin/` sandboxes never show up when you run `git status` for real.
