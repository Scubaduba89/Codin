"""Checks for python-c1-05. Committed and read-only: the checker runs
this against the solution.py in your sandbox. Reading it is allowed."""
import io
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.getcwd())


def bail(msg):
    print(msg)
    raise SystemExit(1)


with redirect_stdout(io.StringIO()):
    import solution

for fname in ("sum_evens", "longest"):
    if not callable(getattr(solution, fname, None)):
        bail("solution.py needs a function named %s - both functions\n"
             "live in this one file." % fname)


def call(label, fn, *args):
    try:
        with redirect_stdout(io.StringIO()):
            return fn(*args)
    except Exception as e:
        bail("%s crashed with %s: %s\n"
             "(the empty list is part of the spec - the right starting\n"
             "value before the loop handles it for free)"
             % (label, type(e).__name__, e))


SUM_CASES = [([1, 2, 3, 4], 6), ([2, 4, 6], 12), ([1, 3, 5], 0),
             ([-4, -3, 7], -4), ([0, 1], 0), ([], 0)]
for nums, want in SUM_CASES:
    got = call("sum_evens(%r)" % (nums,), solution.sum_evens, nums)
    if got != want:
        extra = ""
        if nums == []:
            extra = ("\n(empty list: nothing to add, so the answer is "
                     "the starting total)")
        elif nums == [1, 3, 5]:
            extra = "\n(no evens at all still needs a sensible answer)"
        elif nums == [-4, -3, 7]:
            extra = "\n(negative numbers can be even too: -4 % 2 == 0)"
        bail("sum_evens(%r) returned %r, expected %r.%s"
             % (nums, got, want, extra))

LONG_CASES = [(["hi", "hello", "hey"], "hello"), (["solo"], "solo"),
              (["aa", "bb"], "aa"), ([], "")]
for words, want in LONG_CASES:
    got = call("longest(%r)" % (words,), solution.longest, words)
    if got != want:
        extra = ""
        if words == ["aa", "bb"]:
            extra = ("\n(a tie keeps the FIRST longest - only replace "
                     "your best when the\nnew word is strictly longer)")
        elif words == []:
            extra = "\n(the spec says the empty list returns \"\")"
        bail("longest(%r) returned %r, expected %r.%s"
             % (words, got, want, extra))
print("ok")
