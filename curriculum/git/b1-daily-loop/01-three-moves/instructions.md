Your sandbox holds a tiny git repository called `diary/` - a practice
repo, safe to mangle. Someone left it mid-thought: one file changed,
one brand new.

1. `cd diary`, then ask git what's going on:

       git status

   Read the whole answer. Git sorts the world into: changed but not
   staged, brand new ("untracked"), and staged, ready to commit.

2. Stage everything that's pending (`.` means "all of it, from
   here"):

       git add .

   Run `git status` again - watch the colors change. Nothing is saved
   yet; staging is just choosing.

3. Save the snapshot, with a note to your future self:

       git commit -m "finish today's entry"

   Run `git status` one last time: "working tree clean" is git's way
   of saying *everything is saved*.

4. `python3 codin.py check git-b1-01`

You've been using these moves on the real repo since setup-02. Now
you've seen all three states they move files between - that mental
picture is the whole trick.
