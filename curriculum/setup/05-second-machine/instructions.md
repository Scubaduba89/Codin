Your progress travels by git - so let's give it somewhere to travel.

This one is done on the machine you set up **second**, whichever that
is. It can wait: do it any time during Phase 1, when you actually have
the second machine in front of you. Everything else keeps working
until then.

**If your second machine is an Android phone:**

1. Install **Termux from F-Droid** (f-droid.org). Not the Play Store
   copy - it's outdated and updates can silently break. The README's
   FAQ covers the two Termux quirks worth knowing.

2. Install the tools and sign in to GitHub. Termux starts almost bare,
   so this list is longer than you'd expect - `nano` is an editor and
   `man` is the built-in manual, and later exercises use both:

       pkg install python git gh nano man
       gh auth login

   (Choose GitHub.com → HTTPS → login with a web browser, and follow
   the code it shows you.)

3. Clone the repo **into home** - never into shared storage
   (`~/storage` breaks permissions and git):

       cd ~
       git clone https://github.com/Scubaduba89/Codin codin
       cd codin

**If your second machine is a desktop or laptop:**

1. Make sure `git` and `python3` are installed, and sign in to GitHub
   once (`gh auth login`, or set up an SSH key if you prefer).

2. Clone it wherever you keep projects:

       git clone https://github.com/Scubaduba89/Codin ~/codin
       cd ~/codin

**Then, on either kind of machine:**

4. Name this device and pull your history:

       python3 codin.py doctor --device desktop
       python3 codin.py sync

   (Call it whatever you like - `phone`, `desktop`, `laptop`. The name
   is how the dashboard shows you where each win happened.)

   Watch the XP you earned elsewhere appear here. That's the whole
   platform in one moment: the repo is the truth, and now two machines
   carry it.

5. Verify, from this second machine:

       python3 codin.py check setup-05

6. One last push, so the first machine and the dashboard learn about
   this too:

       python3 codin.py sync

From now on, `python3 codin.py next` on the phone offers something
phone-sized - a guarantee, not a hope: no honest 15-minute Termux
session ends at zero XP.
