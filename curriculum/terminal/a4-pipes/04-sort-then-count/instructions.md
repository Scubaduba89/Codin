A market stall took 24 orders today - `orders.txt`, one fruit per
line, in the order customers shouted them. The question every
shopkeeper asks: how many of each?

The tool is `uniq -c`: it collapses repeated lines and prefixes
each with its count. But uniq has a blind spot you need to see with
your own eyes.

1. Look at the raw orders, then let uniq try:

       cat orders.txt
       uniq -c orders.txt

   A mess - it counts almost everything as 1. Here's why: uniq
   only compares each line with the line DIRECTLY ABOVE it.
   Repeats scattered through the file slip straight past. uniq
   never remembers, it only glances at neighbors.

2. So make the twins stand together first. `sort` lines them up
   alphabetically, then uniq counts honestly:

       sort orders.txt | uniq -c

   Read the pair aloud - "sort, then count" - it's a rhythm you'll
   type for the rest of your life.

3. Save the honest tally:

       sort orders.txt | uniq -c > tally.txt

4. Verify:

       python3 codin.py check terminal-a4-04

`sort | uniq -c` turns ANY list into a frequency table - words,
IP addresses, error codes. Remember the order: sort feeds uniq,
never the other way around.
