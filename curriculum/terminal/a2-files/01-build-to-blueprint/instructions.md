Time to build instead of wander. Two new tools:

    mkdir <name>   - make a directory
    touch <name>   - make an empty file

Your sandbox holds a `blueprint.txt` describing a little website
project. Your job: build the skeleton exactly.

    site/
      index.html
      css/
      img/
      notes/
        todo.txt
      assets/
        fonts/

1. `cd` into your sandbox and read it yourself: `cat blueprint.txt`
2. Start building:

       mkdir site
       cd site
       touch index.html
       mkdir css img notes

   (yes - mkdir happily takes several names at once)

3. `notes/todo.txt` is a file inside a folder you just made. For
   `assets/fonts/`, try the shortcut that builds a whole chain in
   one line:

       mkdir -p assets/fonts

4. `python3 codin.py check terminal-a2-01`

Every project you'll ever start begins exactly like this: an empty
folder, a few mkdirs, a few touches. If the check complains, read
which path it names - that is the piece still missing.
