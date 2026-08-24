Two tiny functions this time - one for numbers, one for text. Small
functions that each do one obvious thing are the bricks Python
programs are built from.

1. In the sandbox, create `solution.py` defining BOTH of these:

   `area(w, h)` returns width times height. Numbers in, number
   out, decimals welcome:

       area(3, 4)    ->  12
       area(2.5, 4)  ->  10.0
       area(0, 7)    ->  0

   `shout(text)` returns the text in ALL CAPS with exactly one `!`
   stuck on the end. Strings know how to uppercase themselves -
   every string carries a `.upper()` method, and `+` glues strings
   together:

       shout("ship it")  ->  "SHIP IT!"
       shout("OK")       ->  "OK!"
       shout("")         ->  "!"     (empty in, just the ! out)

2. Poke both in the Python shell before you check. Feed them odd
   things on purpose - a zero, an empty string - and see what comes
   back. That habit (probe the edges yourself) is the real skill
   this exercise is sneaking in.

       python3
       >>> from solution import area, shout
       >>> area(2.5, 4)
       >>> shout("")

3. python3 codin.py check python-c1-03
