You just did the daily git loop by hand. There's a convenience wrapper
for the routine case - but on this platform, training wheels are
transparent: you get to see exactly what they do.

1. Run the wrapper:

       python3 codin.py sync

   It commits your new progress events, pulls anything from other
   devices, and pushes. That's all it will ever do.

2. Now read it:

       less engine/sync.py

   (Press `q` to leave `less`.) Skip past the error handling and find
   the `run` function. At its heart are three commands - commit, pull,
   push - the same ones you typed by hand last exercise. Everything
   else in that file exists to tell you the truth when git says no.

3. See your progress rendered. Your dashboard is a folder of files in
   `docs/` - serve it locally:

       cd docs && python3 -m http.server 8321

   (Any free port number works - if 8321 is taken on your machine,
   pick another and match it in the address below.)

   Open http://localhost:8321 in a browser: tonight's XP, already on
   the board. Press Ctrl+C in the terminal to stop the server, and
   `cd ..` to come back.

   (Once this repo's GitHub Pages is enabled, the same dashboard also
   lives at your public URL and updates within ~10 minutes of any
   push - check it after this session.)

4. Then:

       python3 codin.py check setup-03
