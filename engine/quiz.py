"""codin quiz <module> - a stdlib input() loop over quizzes/<module>.json.

First pass at >= 80% appends one quiz event (15 XP). Retakes are
always welcome and always free. Exact answers are stored as
normalized sha256 hashes so the bank never contains the answer in
plain text; multiple choice is plain (the phone practice page needs it).
"""

import json
import os
import random
from pathlib import Path

from . import sync as sync_mod
from . import checkers, events, state, ui

PASS_RATIO = 0.8
QUIZ_XP = 15


def bank_path(repo_root, module_id):
    return Path(repo_root) / "quizzes" / ("%s.json" % module_id)


def load_bank(repo_root, module_id):
    path = bank_path(repo_root, module_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def grade(question, answer_text):
    if "choices" in question:
        letters = "abcdefgh"[: len(question["choices"])]
        picked = answer_text.strip().lower()
        if picked not in letters:
            return None  # not an answer; re-ask
        return letters.index(picked) == question["answer"]
    accepted = question.get("accept_shas") or [question["answer_sha"]]
    return checkers.sha_norm(answer_text) in accepted


def ask(question):
    ui.say("")
    ui.say("  " + question["q"])
    if "choices" in question:
        for i, choice in enumerate(question["choices"]):
            ui.say("    %s) %s" % ("abcdefgh"[i], choice))
    elif question.get("hint_format"):
        ui.say(ui.c("    (answer: %s)" % question["hint_format"], "dim"))
    while True:
        answer = input("  > ")
        result = grade(question, answer)
        if result is None:
            ui.say("  (answer with a letter)")
            continue
        return result, answer


def run(repo_root, module_id, replay_state):
    bank = load_bank(repo_root, module_id)
    if bank is None:
        ui.say("No quiz for '%s' (yet)." % module_id)
        return 1
    questions = list(bank["questions"])
    if not os.environ.get("CODIN_QUIZ_NO_SHUFFLE"):  # tests need order
        random.shuffle(questions)
    right = 0
    for q in questions:
        ok, _ = ask(q)
        if ok:
            right += 1
            ui.say(ui.c("  ✔ yes", "green"))
        elif "choices" in q:
            ui.say(ui.c("  ✘ it's %s) %s" % (
                "abcdefgh"[q["answer"]], q["choices"][q["answer"]]), "yellow"))
        else:
            ui.say(ui.c("  ✘ not it - worth revisiting the module", "yellow"))

    score = right / len(questions)
    ui.say("")
    ui.say("  Score: %d/%d" % (right, len(questions)))
    if score < PASS_RATIO:
        ui.say("  Below %d%% - nothing lost. Skim the module, retake any time." %
               int(PASS_RATIO * 100))
        return 0

    already = any(
        ev["type"] == "quiz" and ev["id"] == module_id
        for ev in replay_state["counted"])
    if already:
        ui.say(ui.c("  Passed again - the XP was earned the first time.", "green"))
        return 0
    device = state.device_name(repo_root) or "unknown"
    events.append(repo_root, "quiz", module_id, QUIZ_XP, device)
    ui.say(ui.c("  ✔ Quiz passed  +%d XP" % QUIZ_XP, "green", "bold"))
    ui.say("  (These questions now feed your spaced reviews: they'll come "
           "due in 2 days.)")
    for line in sync_mod.nudge_lines(repo_root):
        ui.say(ui.c("  " + line, "dim"))
    return 0
