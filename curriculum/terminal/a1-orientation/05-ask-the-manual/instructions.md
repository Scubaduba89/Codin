You will never memorize every flag of every command - and you never
have to, because the manual ships with the system:

    ls --help      - quick list of options
    man ls         - the full manual (arrows scroll, `/word` searches,
                     `q` quits)

Your sandbox holds five files of very different sizes. The mission:

1. Using `--help` or `man`, find the `ls` flag that lists files
   **sorted by size, largest first**. (In `man ls`, try typing
   `/size` and Enter to jump to it.)

2. Use it, and save the sorted listing:

       ls -<theflag> > sizes.txt

3. `python3 codin.py check terminal-a1-05`

The habit being planted: when you wonder "can this command do X?",
the answer is one `--help` away - no search engine, no tutor, no
guessing.
