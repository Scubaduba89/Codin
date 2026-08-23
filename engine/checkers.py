"""The check runner and the helper toolkit exercise checkers build on.

Every exercise ships a check.py defining `check(ctx)` (and optionally
`setup(ctx)` for sandbox creation, or `STAGES` for projects). Checkers
verify observable state - files, permissions, git plumbing output,
program behavior - never command history. A failed check raises
CheckFail with a message that names what was expected; it never
contains the answer.
"""

import hashlib
import importlib.util
import os
import re
import shlex
import stat
import subprocess
import sys
from pathlib import Path

from . import sandbox as sandbox_mod

DEFAULT_TIMEOUT = 10


class CheckFail(Exception):
    """Friendly diagnostic for the learner. Never a stack trace."""


class Ctx:
    """Handed to every checker. Helpers raise CheckFail on their own."""

    def __init__(self, repo_root, ex, box):
        self.root = Path(repo_root)
        self.ex = ex
        self.box = Path(box)
        self.exdir = sandbox_mod.exercise_dir(repo_root, ex)

    # --- assertions -------------------------------------------------
    def fail(self, message):
        raise CheckFail(message)

    def require(self, cond, message):
        if not cond:
            raise CheckFail(message)

    # --- filesystem -------------------------------------------------
    def exists(self, rel):
        return (self.box / rel).exists()

    def read(self, rel):
        p = self.box / rel
        self.require(p.exists(), "expected `%s` to exist in your sandbox" % rel)
        return p.read_text(encoding="utf-8")

    def is_executable(self, rel):
        p = self.box / rel
        return p.exists() and bool(p.stat().st_mode & stat.S_IXUSR)

    def mode_bits(self, rel):
        p = self.box / rel
        self.require(p.exists(), "expected `%s` to exist" % rel)
        return stat.S_IMODE(p.stat().st_mode)

    def listdir(self, rel="."):
        p = self.box / rel
        self.require(p.is_dir(), "expected directory `%s` to exist" % rel)
        return sorted(x.name for x in p.iterdir())

    # --- processes --------------------------------------------------
    def run(self, cmd, cwd=None, stdin=None, timeout=DEFAULT_TIMEOUT, env=None):
        """Run a command list inside the sandbox. -> CompletedProcess.
        Times out safely; never raises on nonzero exit."""
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        merged_env = dict(os.environ)
        if env:
            merged_env.update(env)
        try:
            return subprocess.run(
                cmd, cwd=str(cwd or self.box), input=stdin,
                capture_output=True, text=True, timeout=timeout,
                env=merged_env,
            )
        except subprocess.TimeoutExpired:
            raise CheckFail(
                "`%s` ran for more than %ds - likely an infinite loop. "
                "Stop it, rethink, retry." % (" ".join(cmd), timeout))
        except FileNotFoundError:
            raise CheckFail("command not found: %s" % cmd[0])

    def run_bash(self, script, cwd=None, timeout=DEFAULT_TIMEOUT):
        return self.run(["bash", "-c", script], cwd=cwd, timeout=timeout)

    def git(self, *args, cwd=None):
        """Git plumbing in the sandbox (or cwd). -> stdout, stripped."""
        r = self.run(["git"] + list(args), cwd=cwd, timeout=30)
        self.require(
            r.returncode == 0,
            "git %s failed here: %s" % (args[0], r.stderr.strip() or "(no output)"))
        return r.stdout.strip()

    # --- exercise-type helpers -------------------------------------
    def run_python_tests(self, tests="tests.py"):
        """Run the exercise's committed test file against the learner's
        solution in the sandbox. Exit code decides; output becomes the
        diagnostic."""
        tests_path = self.exdir / tests
        r = self.run([sys.executable, str(tests_path)], timeout=15)
        if r.returncode != 0:
            tail = (r.stdout + r.stderr).strip().splitlines()
            raise CheckFail("\n".join(tail[-12:]) or "tests failed with no output")

    def compile_c(self, sources, out="prog"):
        """Compile C sources in the sandbox with cc. -> path to binary."""
        srcs = [str(self.box / s) for s in sources]
        r = self.run(["cc", "-Wall", "-O0", "-o", out] + srcs, timeout=30)
        if r.returncode != 0:
            raise CheckFail("it doesn't compile yet:\n" +
                            "\n".join(r.stderr.strip().splitlines()[-10:]))
        return self.box / out

    def clone_bundle(self, bundle_rel, dest="repo"):
        """Materialize a git repo from a committed .bundle fixture."""
        bundle = self.exdir / bundle_rel
        target = self.box / dest
        if not target.exists():
            r = self.run(["git", "clone", "-q", str(bundle), str(target)], timeout=30)
            self.require(r.returncode == 0, "could not unpack the practice repo")
            self.run(["git", "config", "user.name", "Codin Learner"], cwd=target)
            self.run(["git", "config", "user.email", "learner@codin.local"], cwd=target)
        return target

    def grep(self, rel, pattern):
        return re.search(pattern, self.read(rel), re.MULTILINE)


def sha_norm(text):
    """Normalized hash for exact-answer grading: trim, lowercase,
    collapse inner whitespace."""
    norm = " ".join(str(text).strip().lower().split())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def load_checker(repo_root, ex):
    path = sandbox_mod.exercise_dir(repo_root, ex) / "check.py"
    if not path.exists():
        raise CheckFail("this exercise has no checker yet - it's a stub")
    spec = importlib.util.spec_from_file_location(
        "codin_check_" + ex["id"].replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_check(repo_root, ex, checker, box):
    """-> (True, celebration_note or None) on pass; raises CheckFail."""
    ctx = Ctx(repo_root, ex, box)
    note = checker.check(ctx)
    return True, note if isinstance(note, str) else None


def stage_list(checker):
    """Projects define STAGES = [(name, fn), ...]."""
    return list(getattr(checker, "STAGES", []))
