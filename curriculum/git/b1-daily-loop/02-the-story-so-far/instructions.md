A repo isn't just files - it's the whole story of the files. Your
sandbox has a `recipe/` repo with some history already in it.

1. `cd recipe` and read the story so far:

       git log --oneline

   One line per commit, newest on top.

2. The recipe calls for butter, and you've gone Mediterranean. Open
   `recipe.txt` with `nano` and change the word `butter` to
   `olive oil`. Save and exit.

3. Before committing, see EXACTLY what you changed:

       git diff

   Minus lines are the old text, plus lines are the new. Reading a
   diff before every commit is the habit that catches a thousand
   future mistakes. (`q` exits if it opens a pager.)

4. Commit the change with a message that says what happened - then
   read the story again:

       git add recipe.txt
       git commit -m "swap butter for olive oil"
       git log --oneline

5. Count the commits in the log, and record the number back at the
   sandbox's top level (one `cd ..` up):

       echo 3 > answer.txt

   ...if 3 is what you counted, that is.

6. `python3 codin.py check git-b1-02`
