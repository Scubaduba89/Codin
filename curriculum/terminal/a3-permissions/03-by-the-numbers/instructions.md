chmod speaks a second dialect: numbers. Each right has a price -

    r = 4      w = 2      x = 1

Add them up inside each trio, then read the three sums in order:
owner, group, others. So `rw- r-- ---` is 6,4,0 - mode 640. And
`rwx r-x r-x` is 7,5,5 - mode 755. One short number states the
whole rulebook, which is why READMEs and deploy guides love it.

Two files in your sandbox wear the wrong modes:

- `secrets.txt` is currently readable AND writable by everyone
  on the machine. Tighten it to exactly 640
  (owner rw, group read-only, others nothing).
- `deploy.sh` is a script that nobody can run. Open it up to
  exactly 755 (owner rwx, group and others r-x).

The move, once per file:

    chmod 640 secrets.txt

...and the same shape for deploy.sh with its number. Check your
work with `ls -l`: can you read 640 and 755 back off the trios?

Then: `python3 codin.py check terminal-a3-03`

Letters tweak one right at a time; numbers set the whole rulebook
in one stroke. You'll use both, usually within the same week.
