A loop plus a running answer is half of all code you will ever
write: start with a blank answer, walk the list, update the answer
whenever an item earns it. Two functions, same pattern twice.

1. In the sandbox, create `solution.py` defining BOTH functions.

   `sum_evens(nums)` takes a list of whole numbers and returns the
   sum of just the even ones. Even means the remainder when
   dividing by 2 is zero - in Python, `n % 2 == 0` - and negatives
   count too (-4 is even). The full spec:

       sum_evens([1, 2, 3, 4])   ->  6
       sum_evens([1, 3, 5])      ->  0
       sum_evens([-4, -3, 7])    ->  -4
       sum_evens([])             ->  0    (nothing to add)

   `longest(words)` takes a list of strings and returns the
   longest one. On a tie, the one that appears FIRST wins. The
   empty list is a decision, and this spec decides it:

       longest(["hi", "hello", "hey"])  ->  "hello"
       longest(["aa", "bb"])            ->  "aa"  (tie: first)
       longest([])                      ->  ""   (empty string)

2. The pattern for both: set a starting value BEFORE the loop
   (`0` for a total, `""` for a best-so-far), then

       for item in the_list:

   and update your answer inside when the item deserves it. Get
   the empty cases free by choosing the right starting value.

3. Poke both in the Python shell with the exact lists above -
   empties included - before you check. If you're unsure what the
   checker wants, the judge itself is readable:
   `curriculum/python/c1-refresher/05-loops-and-lists/tests.py`.
   Reading tests is fair play; it's how working devs learn specs.

4. python3 codin.py check python-c1-05
