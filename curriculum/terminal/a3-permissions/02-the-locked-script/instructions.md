Your sandbox holds `locked.sh` - a finished, working script. Try
to run it (`./` means "the one right here, in this directory"):

    ./locked.sh

The shell refuses: `Permission denied`. Read that error and take
it literally - the file exists, the code inside is fine, but its
rulebook has no `x`. Nobody may run it. Grant the right with
chmod's symbolic dialect:

    chmod u+x locked.sh

That reads "user (the owner): add execute". Run `ls -l` before and
after if you want to watch the `x` appear in the rulebook. Now run
the script again, and this time keep the proof:

    ./locked.sh > output.txt

Then: `python3 codin.py check terminal-a3-02`

The dialect generalizes: `g` is the group, `o` is others, `a` is
all of them; `-` revokes just as `+` grants (try `chmod a-w` on
something precious one day). Every script you will ever write is
born un-runnable. `chmod u+x` is the spell that wakes it - worth
having in your fingers forever.
