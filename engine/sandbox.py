"""Exercise sandboxes under .codin/sandbox/<exercise-id>/.

A sandbox is disposable practice ground: `codin start` builds it,
`codin reset` rebuilds it from scratch. Resetting never touches the
event log - work is never lost, only workspaces.
"""

import shutil
from pathlib import Path

from . import state


def path(repo_root, ex_id):
    return state.dir_(repo_root) / "sandbox" / ex_id


def exercise_dir(repo_root, ex):
    return Path(repo_root) / ex["dir"]


def materialize(repo_root, ex, checker=None):
    """Create the sandbox: copy fixture/ if present, then run the
    checker module's optional setup(ctx). Idempotent - an existing
    sandbox is left alone."""
    box = path(repo_root, ex["id"])
    if box.exists():
        return box, False
    box.mkdir(parents=True)
    fixture = exercise_dir(repo_root, ex) / "fixture"
    if fixture.is_dir():
        shutil.copytree(fixture, box, dirs_exist_ok=True)
    if checker is not None and hasattr(checker, "setup"):
        from .checkers import Ctx  # local import to avoid a cycle

        checker.setup(Ctx(repo_root, ex, box))
    return box, True


def reset(repo_root, ex, checker=None):
    box = path(repo_root, ex["id"])
    if box.exists():
        shutil.rmtree(box)
    return materialize(repo_root, ex, checker)
