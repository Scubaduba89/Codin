#!/bin/bash
# Regressions for the first-run bugs found on 2026-09-04, when a real
# first win showed in the CLI but never reached the dashboard.
# Run from anywhere:  bash tests/regress_firstrun.sh
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"; S="$(mktemp -d)"
mkdir -p "$S/src"
(cd "$SRC" && tar cf - --exclude=.git --exclude=.codin --exclude=__pycache__ .) | (cd "$S/src" && tar xf -)
git -C "$S/src" init -q -b main
git -C "$S/src" -c user.name=S -c user.email=s@x add -A
git -C "$S/src" -c user.name=S -c user.email=s@x commit -qm seed
git clone -q --bare "$S/src" "$S/remote.git"
git clone -q "$S/remote.git" "$S/phone"
cd "$S/phone"; git config user.name Adam; git config user.email a@x
fail() { echo "REGRESS FAIL: $1"; exit 1; }

echo "== 1. phone-first: doctor is green and proves it can publish =="
python3 codin.py doctor --device phone > out.txt 2>&1
grep -q "can publish to GitHub" out.txt || fail "no publish check in doctor"
grep -q "All green" out.txt || { cat out.txt; fail "doctor not green"; }

echo "== 2. first win nudges about publishing (the reported incident) =="
python3 codin.py check setup-01 > out.txt 2>&1
grep -q "This win is on this machine only" out.txt || { cat out.txt; fail "no first-win sync nudge"; }

echo "== 3. next on the phone never dead-ends on setup-05 =="
python3 codin.py next > out.txt 2>&1
grep -q "setup-05" out.txt && { cat out.txt; fail "next still pins to setup-05"; }
grep -q "start setup-02" out.txt || { cat out.txt; fail "next should offer setup-02"; }

echo "== 4. sync failure is loud, honest, and never a traceback =="
git remote set-url origin "$S/nonexistent.git"
python3 codin.py sync > out.txt 2>&1 || true
grep -qi "traceback" out.txt && { cat out.txt; fail "sync raised a traceback"; }
grep -q "NOT on GitHub" out.txt || { cat out.txt; fail "sync did not say it failed to publish"; }
grep -q "git said" out.txt || { cat out.txt; fail "sync hid git's message"; }
python3 -c "import json;d=json.load(open('.codin/last_sync.json'));assert d['pushed'] is False" || fail "marker not recorded on failure"
git remote set-url origin "$S/remote.git"

echo "== 5. re-checking a passed exercise never reads as failure =="
python3 codin.py sync >/dev/null 2>&1
python3 codin.py check setup-03 >/dev/null 2>&1 || true
python3 codin.py check setup-03 > out.txt 2>&1
code=$?
grep -qE "Already earned|Still passes|PASS" out.txt || { cat out.txt; fail "re-check reads as failure"; }
[ $code -eq 0 ] || fail "re-check exited nonzero"

echo "== 6. sync commit does not sweep unrelated staged work =="
echo "half-finished thought" > scratch-note.txt; git add scratch-note.txt
python3 codin.py check setup-04 >/dev/null 2>&1 || true
python3 codin.py tutor-mark lesson >/dev/null; python3 codin.py tutor-mark hint >/dev/null
python3 codin.py check setup-04 >/dev/null 2>&1
python3 codin.py sync >/dev/null 2>&1
git show --name-only --format= HEAD | grep -q "scratch-note" && fail "sync swept unrelated staged file"
git diff --cached --name-only | grep -q "scratch-note" || fail "staged file was lost"

echo "== REGRESSIONS: ALL GREEN =="
