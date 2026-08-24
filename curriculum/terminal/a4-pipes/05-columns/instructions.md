A lot of Unix data is a table in disguise: one record per line,
fields split by a separator character. Your sandbox has the crew
roster of a small ship, `crew.txt`, three fields split by colons:

    name:role:home port

`cut` slices columns out of such lines. Two flags do all the work:
`-d` names the delimiter (the separator), `-f` picks which field.

1. Look at the roster, then slice out just the names:

       cat crew.txt
       cut -d: -f1 crew.txt

   Read the flags aloud: "delimiter colon, field one". Save it:

       cut -d: -f1 crew.txt > names.txt

2. Now the third column - every sailor's home port:

       cut -d: -f3 crew.txt > ports.txt

3. Verify:

       python3 codin.py check terminal-a4-05

This shape is everywhere. On desktop Linux, peek at `/etc/passwd`
sometime: every account on your machine, colon-delimited, and
`cut -d: -f1 /etc/passwd` lists them all. Same command you just
learned - real system file.
