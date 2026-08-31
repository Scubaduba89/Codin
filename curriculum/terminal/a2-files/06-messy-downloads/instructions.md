The boss fight. Your sandbox holds a `downloads/` folder in the
state every real one reaches eventually: eighteen files, four
kinds, zero order. Some names contain spaces and parentheses -
names you'd hate to type, which is exactly why the globs you just
learned are about to feel like a superpower.

The goal: `ls downloads` shows ONLY four folders, no loose files.

    images/     every .jpg and .png
    pdfs/       every .pdf
    text/       every .txt
    archives/   every .zip and .tar.gz

1. Walk in and survey the damage:

       cd downloads
       ls

2. Build the four homes (one mkdir can make them all).

3. Sweep, one kind at a time. Look first, then move:

       ls *.jpg
       mv *.jpg images/
       mv *.png images/

   Carry on with `*.pdf`, `*.txt`, `*.zip`, `*.gz`. The shell
   expands each pattern into the real names - spaces, parentheses
   and all - so you never type them and never mistype them.

4. Final survey: `ls` shows just the four folders. Then:

       python3 codin.py check terminal-a2-06

Wrong home? mv it again - moving twice is free. Board hopelessly
confusing? `python3 codin.py reset terminal-a2-06` deals a fresh
mess, and no progress is ever lost to a reset.
