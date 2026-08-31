`grep` prints every line of a file that contains a given word (it's
case-sensitive: ERROR and error are strangers). Sixty days of a
ship's log sit in your sandbox as `ship-log.txt`. Most days were
fine. Some were not.

1. Skim the haystack:

       cat ship-log.txt

2. Pull out only the bad days:

       grep ERROR ship-log.txt

   Every line containing ERROR, nothing else. Save them:

       grep ERROR ship-log.txt > trouble.txt

3. Now flip it. `-v` inverts the match - print the lines that do
   NOT contain the word:

       grep -v ERROR ship-log.txt > smooth.txt

   Two files: one is the trouble, one is everything else, and
   together they're the whole log again.

4. Verify:

       python3 codin.py check terminal-a4-03

Why it matters: real logs run to millions of lines, and nobody
reads them. They grep them. You just did, at scale one-tiny-ship.
