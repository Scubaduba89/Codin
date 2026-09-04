You spent the shell track running other people's programs. From here
on, you are the one writing them. This module knocks the rust off
the Python you once started - briskly, one small win at a time.

1. `cd` into your sandbox (the start screen printed its path) and
   create your program:

       nano solution.py

   (Any editor is fine. If `nano` isn't installed yet: `pkg install
   nano` on the phone, or use whatever editor you already like.)

2. Near the top, define a variable:

       NAME = "..."

   Put a real name - yours works - between the quotes. A variable
   is just a label stuck on a value so you can use it by name.

3. Below it, print a greeting that USES the variable, so the output
   changes whenever NAME does. That's what f-strings are for: an
   `f` before the opening quote, and anything inside `{braces}` is
   swapped for its value. For example, this prints `3 coins`:

       print(f"{count} coins")

   Your program must print exactly one line, shaped like this:

       Hello, <whatever NAME holds>!

   Capital H, a comma, one space, and a `!` on the end.

4. Run it yourself before checking - always run it yourself first:

       python3 solution.py

   If Python complains, read the message from the bottom up: the
   last line says what went wrong, the lines above say where. That
   message is reading material, not a slap.

5. When the output looks right:

       python3 codin.py check python-c1-01
