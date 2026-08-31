Your sandbox holds `access.log`: 150 requests to a small web
server, one per line, in the exact format real servers write.
The FIRST space-separated column of every line is the visitor's
IP address. Look:

    head access.log

Somebody is hammering this server. Find out who.

THE MISSION - one pipeline, producing the top 5 IP addresses by
request count, landed in `top5.txt`. Every stage is a tool you
now own:

    cut        slice out the IP column
    sort       stand the twins together
    uniq -c    collapse and count them
    sort -rn   reorder by the count: -n compares as numbers,
               -r flips to biggest-first
    head -5    keep only the top five
    >          land the result in top5.txt

Build it a stage at a time - run the first command alone, look at
what comes out, add `| sort`, look again, keep going. Watching the
data change shape at every `|` is how pipelines are really written,
even by people who've done it for twenty years.

One hint for stage one: the log's columns are separated by spaces,
and a space must be quoted to survive the shell, like so: -d' '

When top5.txt exists:

    python3 codin.py check terminal-a4-06

Know two things before you start. First: this exact problem is
coming back for you twice - once in Python, once in C. Same log,
same top five, three languages: that's the Polyglot badge thread,
and today's one-liner is the yardstick the other two get measured
against. Second: this is not a toy. On a real server this very
pipeline is how an admin finds the attacker at 3am - one line, no
code, answer in milliseconds.
