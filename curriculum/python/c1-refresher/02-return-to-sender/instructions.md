`print` shows a value to a human and then it's gone. `return` hands
the value back to the code that asked, which can store it, reuse it,
or build on it. Nearly every function you will ever write returns.

1. In this exercise's sandbox, create `solution.py` with one
   function in it:

       def greet(name):
           ...

   (`def` starts a function; `name` is the value handed in; the
   indented body is what runs when someone calls it.)

2. `greet` must RETURN - not print - exactly this string:

       Welcome back, <name>!

   So calling greet("Ada") gives back "Welcome back, Ada!".
   Capital W, one space after the comma, `!` at the end, and
   nothing printed to the screen.

3. Test-drive it in the interactive Python shell (Ctrl-D leaves):

       python3
       >>> from solution import greet
       >>> greet("Ada")

   The shell echoes the returned value back at you. If you see
   `None` (or the greeting appears WITHOUT quotes around it), your
   function printed instead of returning - the value escaped out
   the screen instead of coming back to the caller.

4. python3 codin.py check python-c1-02
