"""Discover and validate curriculum content.

Layout: curriculum/<track-dir>/<module-dir>/module.json plus one
subdirectory per exercise containing meta.json (+ instructions.md,
check.py, optional fixture/). Modules with no exercise dirs are stubs -
they appear on the map (fogged) but can't be started.
"""

import json
from pathlib import Path

MODULE_FIELDS = ("id", "track", "title", "phase", "order", "summary")
EXERCISE_FIELDS = ("id", "title", "type", "minutes", "phone", "xp")
EXERCISE_TYPES = {"micro", "standard", "challenge", "project", "gate", "quiz"}


class ContentError(Exception):
    pass


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        raise ContentError("%s: invalid JSON (%s)" % (path, e))


def load_curriculum(repo_root):
    """-> {"modules": [module dicts with "exercises" and "dir"]}, ordered
    by (phase, order). Raises ContentError on malformed content."""
    root = Path(repo_root) / "curriculum"
    modules = []
    # Single-module areas sit at curriculum/<module>/ (setup, gates);
    # tracks sit at curriculum/<track>/<module>/.
    found = sorted(root.glob("*/module.json")) + sorted(root.glob("*/*/module.json"))
    for mod_json in found:
        mod_dir = mod_json.parent
        if mod_dir.name.startswith("_"):
            continue
        mod = _read_json(mod_json)
        for field in MODULE_FIELDS:
            if field not in mod:
                raise ContentError("%s: missing '%s'" % (mod_json, field))
        mod.setdefault("requires", [])
        mod.setdefault("elective", False)
        mod.setdefault("no_bonus", False)
        mod["dir"] = str(mod_dir.relative_to(repo_root))
        mod["exercises"] = []
        for meta_json in sorted(mod_dir.glob("*/meta.json")):
            ex = _read_json(meta_json)
            for field in EXERCISE_FIELDS:
                if field not in ex:
                    raise ContentError("%s: missing '%s'" % (meta_json, field))
            if ex["type"] not in EXERCISE_TYPES:
                raise ContentError("%s: unknown type '%s'" % (meta_json, ex["type"]))
            ex.setdefault("requires", [])
            ex["module"] = mod["id"]
            ex["dir"] = str(meta_json.parent.relative_to(repo_root))
            mod["exercises"].append(ex)
        modules.append(mod)

    modules.sort(key=lambda m: (m["phase"], m["order"]))

    seen = set()
    for mod in modules:
        for key in [mod["id"]] + [ex["id"] for ex in mod["exercises"]]:
            if key in seen:
                raise ContentError("duplicate id: %s" % key)
            seen.add(key)
    return {"modules": modules}


def exercise_map(curriculum):
    return {
        ex["id"]: ex for mod in curriculum["modules"] for ex in mod["exercises"]
    }


def module_map(curriculum):
    return {mod["id"]: mod for mod in curriculum["modules"]}


def find(curriculum, some_id):
    """Look up an id as exercise first, then module. -> (kind, obj) or
    (None, None)."""
    ex = exercise_map(curriculum).get(some_id)
    if ex:
        return "exercise", ex
    mod = module_map(curriculum).get(some_id)
    if mod:
        return "module", mod
    return None, None


def requirements_met(curriculum, obj, state):
    """Check an exercise's or module's `requires` list against replay
    state. Entries may be exercise ids (need a counted done event) or
    module ids (need completion). -> (ok, [unmet ids])."""
    mods = module_map(curriculum)
    completed = set(state["completed_modules"])
    unmet = []
    for req in obj.get("requires", []):
        if req in mods:
            if req not in completed:
                unmet.append(req)
        elif req not in state["done"]:
            unmet.append(req)
    return (not unmet), unmet


def unlocked(curriculum, ex, state):
    """An exercise is unlocked when its module's requires and its own
    requires are all met."""
    mod = module_map(curriculum)[ex["module"]]
    ok_mod, unmet_mod = requirements_met(curriculum, mod, state)
    ok_ex, unmet_ex = requirements_met(curriculum, ex, state)
    return (ok_mod and ok_ex), unmet_mod + unmet_ex
