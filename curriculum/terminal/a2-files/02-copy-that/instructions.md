`cp` copies. The original stays put; a clone appears where you aim:

    cp <file> <destination-folder>/

Your sandbox: a poem in `notes/`, a `photos/` folder (one photo
hides in a subfolder), and an empty `backup/`.

1. Copy the poem into the backup:

       cp notes/poem.txt backup/

2. Now try to copy the whole photos folder the same way:

       cp photos backup/

   Read the complaint - it's short and it's honest. Plain cp
   refuses folders. Add `-r` (recursive: the folder and everything
   inside, all the way down):

       cp -r photos backup/

3. Verify nothing MOVED: `ls notes photos` - every original must
   still be there. That is the whole point of cp.

4. `python3 codin.py check terminal-a2-02`

"Let me try that on a copy first" is one of the great survival
instincts of computing. This is the command behind it.
