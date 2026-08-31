Time to write a program. A real one, from scratch, that your
operating system will run for you.

1. In your sandbox, open a brand-new file in the editor:

       nano mine.sh

2. Type these three lines (add more echoes if you like, but keep
   these two lines in it, exactly):

       #!/bin/sh
       echo "made by hand"
       echo "run by the kernel"

   Save and exit: Ctrl+O, Enter, then Ctrl+X.

3. That first line is the SHEBANG, and it is not decoration. When
   you run a file, the KERNEL - the core of the operating system
   itself - peeks at the file's first bytes. If they are `#!`, it
   reads the rest of that line as the answer to "which program
   understands this file?" and starts that interpreter for you.
   `#!/bin/sh` says "feed me to the shell"; a Python script would
   open with `#!/usr/bin/env python3`. This little line is your
   first direct handshake with the kernel.

4. New scripts are born un-runnable. You know the fix by now:

       chmod u+x mine.sh

5. Run it, and capture the proof:

       ./mine.sh > proof.txt

   (`./` means "this one, right here" - for a bare name the shell
   searches only its PATH list, and your sandbox isn't on it.)

Then: `python3 codin.py check terminal-a3-04`

If the check grumbles, read its words slowly: it will point at the
shebang, the x bit, or the output. Errors are directions, not
verdicts.
