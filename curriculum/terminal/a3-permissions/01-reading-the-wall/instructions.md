Every file on Linux carries a tiny rulebook: who may read it, who
may write it, who may run it as a program. `ls -l` (long listing)
shows the rulebooks:

    ls -l

Each line starts like `-rw-r--r--`. Skip the very first character
(`-` file, `d` directory). The remaining nine read as three trios:

    rw-   r--   r--
    owner group others (= everyone else)

`r` may read, `w` may write (change or empty it), `x` may run it.
A `-` in a slot means "no".

Your sandbox holds three files with three different rulebooks. Run
`ls -l`, decode the trios, and answer three questions in a file
named `answers.txt` - one answer per line, nothing else:

    line 1: which file can ONLY its owner read? (the filename)
    line 2: which file could be run as a program? (the filename)
    line 3: may "others" write to bulletin.txt? (yes or no)

Build the file with echo - `>` starts it, `>>` appends a line:

    echo "somefile.txt" > answers.txt
    echo "otherfile.sh" >> answers.txt
    echo "yes" >> answers.txt

(Those are format examples, not the answers - trust your ls -l.)

Then: `python3 codin.py check terminal-a3-01`

Why care? Half of all "why won't this work?" moments on Linux are
a permission quietly saying no. After today you can read the no.
