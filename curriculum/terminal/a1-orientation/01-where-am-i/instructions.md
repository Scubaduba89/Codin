Your sandbox contains a little town. Somewhere in it is a room with a
`chest.txt`. Your three tools:

    pwd     - print where you are
    ls      - list what's here
    cd      - move (cd harbor, cd .., cd = go home)

1. `cd` into your sandbox (the start screen printed its path).
2. Wander: `ls` to look around, `cd somewhere` to walk, `pwd` any
   time you're lost, `cd ..` to step back out.
3. When you're standing in the room that contains `chest.txt`, leave
   proof you were there:

       pwd > path.txt

   (That writes your current location into a file, in that room.)

4. From anywhere: `python3 codin.py check terminal-a1-01`

Lost? `cd` with nothing after it teleports you home - then cd back
into the sandbox and try again. You cannot break anything in here.
