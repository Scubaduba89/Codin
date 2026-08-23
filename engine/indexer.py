"""Regenerate the dashboard's data files from curriculum sources.

`codin index` runs this explicitly (never automatically) after content
is added or edited. Output is deterministic so diffs stay clean.

- docs/data/curriculum.json: the full module/exercise index the
  dashboard and the fixture-checked engines consume.
- docs/data/quizzes/<module>.json: multiple-choice-only mirrors for the
  phone practice page (exact-answer questions are listed by key only, so
  the dashboard can count review items without ever seeing answers).
"""

import json
from pathlib import Path

from . import content


def _strip(mod):
    keep = (
        "id", "track", "title", "phase", "order", "summary",
        "requires", "elective", "no_bonus",
    )
    out = {k: mod[k] for k in keep}
    out["exercises"] = [
        {
            k: ex[k]
            for k in ("id", "title", "type", "minutes", "phone", "xp", "requires")
        }
        for ex in mod["exercises"]
    ]
    return out


def write_index(repo_root):
    """-> (curriculum, [written paths])"""
    repo_root = Path(repo_root)
    curriculum = content.load_curriculum(repo_root)
    written = []

    index = {"modules": [_strip(m) for m in curriculum["modules"]]}
    out = repo_root / "docs" / "data" / "curriculum.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")
    written.append(out)

    mirror_dir = repo_root / "docs" / "data" / "quizzes"
    for quiz_path in sorted((repo_root / "quizzes").glob("*.json")):
        quiz = json.loads(quiz_path.read_text(encoding="utf-8"))
        mirror = {"module": quiz["module"], "questions": []}
        for q in quiz["questions"]:
            if q.get("choices"):
                mirror["questions"].append(
                    {
                        "key": q["key"],
                        "q": q["q"],
                        "choices": q["choices"],
                        "answer": q["answer"],
                    }
                )
            else:
                mirror["questions"].append({"key": q["key"]})
        mirror_dir.mkdir(parents=True, exist_ok=True)
        out = mirror_dir / quiz_path.name
        out.write_text(json.dumps(mirror, indent=1) + "\n", encoding="utf-8")
        written.append(out)
    return curriculum, written
