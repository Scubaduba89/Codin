Plain `ls` doesn't show everything: files whose names start with a dot
are hidden. Your sandbox has three rooms; ONE of them hides a dotfile,
and inside it is a single secret word.

1. Explore the rooms. In each one, compare:

       ls
       ls -a

   (`.` is the room you're in, `..` is the way you came - they show
   up everywhere. You're hunting for a third dot-thing.)

2. Read the hidden file with `cat <name>`.

3. Back at the sandbox's front door (its top folder), write the
   secret word into an answer file:

       echo "theword" > answer.txt

4. `python3 codin.py check terminal-a1-02`

Almost all Linux configuration lives in dotfiles like this - your
home directory is full of them. Now you can see them.
