Programs earn their keep by choosing. An `if / elif / else` chain
walks down a ladder of conditions and runs ONLY the first rung
whose condition is true - everything after it is skipped.

1. In the sandbox, create `solution.py` defining `classify(n)`,
   which returns one of exactly four strings:

       "negative"   when n is below 0
       "zero"       when n is exactly 0
       "small"      when n is 1 through 9
       "big"        when n is 10 or more

   Lowercase, spelled exactly like that. The shape you want is one
   `if`, a couple of `elif` rungs, and an `else` at the bottom.
   (`==` asks "equal?"; a single `=` assigns - a classic mixup.)

2. The interesting part is the boundaries. Before you check, say
   out loud what YOUR code returns for -1, 0, 1, 9 and 10, then
   verify in the Python shell:

       python3
       >>> from solution import classify
       >>> classify(9)
       >>> classify(10)

   `<` and `<=` are one keystroke apart and a whole bug apart.
   Off-by-one boundary slips like that live in real production
   code everywhere; this is where you train the eye for them.

3. python3 codin.py check python-c1-04
