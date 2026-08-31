A path starting with `/` is absolute - directions from the planet's
core, same from anywhere. Anything else is relative - directions from
where you're standing. `..` means "one step back toward the root".

Your sandbox has two neighboring buildings:

    bakery/oven/
    florist/counter/

The drill - deliver a note WITHOUT walking next door:

1. `cd` into `bakery/oven`.
2. From in there, in one command, drop a file into the florist's
   counter using a relative path (step out, out, across, in):

       echo "warm bread says hi" > ../../florist/counter/note.txt

   Count the hops before you run it: oven → bakery → sandbox →
   florist → counter.

3. Still standing in the oven, check your aim from a distance:

       ls ../../florist/counter

4. `python3 codin.py check terminal-a1-04`

If the note landed somewhere weird, `ls` around, delete strays with
`rm`, and re-aim. Mis-thrown paths are how everyone learns `..`.
