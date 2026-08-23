Your progress travels by git - so let's give it somewhere to travel.
This exercise is done ON YOUR PHONE (or any second machine), any time
during Phase 1. No rush.

On an Android phone:

1. Install **Termux from F-Droid** (f-droid.org). Not the Play Store
   copy - it's outdated and updates can silently break. The README's
   FAQ covers the two Termux quirks worth knowing.

2. In Termux, install the tools and sign in to GitHub:

       pkg install python git gh
       gh auth login

   (Choose GitHub.com → HTTPS → login with a web browser, and follow
   the code it shows you.)

3. Clone the repo **into home** - never into shared storage
   (`~/storage` breaks permissions and git):

       cd ~
       git clone https://github.com/Scubaduba89/Codin codin
       cd codin

4. Name this device and pull your history:

       python3 codin.py doctor --device phone
       python3 codin.py sync

   Watch your desktop XP appear on the phone. That's the whole
   platform in one moment: the repo is the truth, and now two
   machines carry it.

5. Verify, from the phone:

       python3 codin.py check setup-05

From now on, `python3 codin.py next` on the phone offers something
phone-sized - a guarantee, not a hope: no honest 15-minute Termux
session ends at zero XP.
