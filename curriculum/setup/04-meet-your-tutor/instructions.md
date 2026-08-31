This repo comes with a tutor: Claude Code, with a strict teaching
persona baked in. It guides - it never solves. Worth meeting before
the real exercises begin.

1. In a terminal at the repo root, start Claude Code:

       claude

2. Ask for a lesson:

       /lesson

   The tutor will introduce itself and walk you into whatever is next
   for you. Notice what it does NOT do: it won't type answers into
   your files, and it won't hand you commands to paste for graded
   work. Its hints climb a ladder - nudge first, concept second,
   worked example on *different* data third. The last rung is never
   "the answer".

3. Try the hint ladder once, just to see the shape:

       /hint

4. Leave Claude (Ctrl+C or /exit) and verify:

       python3 codin.py check setup-04

One honest note, tutor-to-learner: you could ask any AI to just do
these exercises. It would work, and it would teach you nothing - this
repo exists to train the skill you can't delegate. The tutor holds
that line so you don't have to.
