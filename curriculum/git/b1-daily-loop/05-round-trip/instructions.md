Everything so far lived on one machine. The daily loop's last two
moves - pull and push - are how repos trade history across machines.

Your sandbox simulates your whole world in miniature: a `local/` repo
(your machine) wired to a `github.git` remote (the cloud). And while
you weren't looking, *another machine pushed something to the remote*.
Your local copy doesn't know yet.

1. `cd local`, then look around:

       git log --oneline
       ls

   No news anywhere. Now ask the remote for anything you're missing:

       git pull

   Read what it prints, then `ls` and `git log --oneline` again -
   a file called `news.txt` arrived, carried inside a commit. That's
   exactly what happens when your phone pulls your desktop's XP.

2. Your turn to send something back. Write a reply and walk the loop:

       echo "got the news, all quiet here" > reply.txt
       git add reply.txt
       git commit -m "reply to the news"
       git push

3. `python3 codin.py check git-b1-05`

The order matters and now you've felt why: pull FIRST, so your push
builds on everything the remote knows. It's the exact dance
`python3 codin.py sync` performs on this repo - fifteen lines you've
already read.
