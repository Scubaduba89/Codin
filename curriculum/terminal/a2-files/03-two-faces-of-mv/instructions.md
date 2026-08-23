`mv` has two faces, one syntax:

    mv old-name new-name    - rename (destination is a new name)
    mv file some-folder/    - move   (destination is a folder)

Your sandbox: a misspelled `repotr.txt`, a `receipt.txt`, and an
`archive/` folder.

1. Face one - rename the typo away:

       mv repotr.txt report.txt

2. Face two - file the receipt:

       mv receipt.txt archive/

3. Look at your work: `ls` then `ls archive`. The report stays at
   the top under its fixed name; the receipt now lives in the
   archive; nothing is left over.

4. `python3 codin.py check terminal-a2-03`

There is no separate "rename" command in the shell - this is it.
The trailing `/` on a destination is a good habit: it says "into
that folder" unmistakably, and it fails loudly (instead of
renaming!) if the folder doesn't exist.
