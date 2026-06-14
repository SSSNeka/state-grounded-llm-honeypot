"""Authoritative session-state engine.

WEEK 1 SCAFFOLD: this is a minimal, runnable skeleton. It models just enough
state (cwd, a tiny virtual filesystem, environment variables, last exit code)
to (a) prove the snapshot/grounding flow end-to-end and (b) give the team a
stable interface to build against.

The full engine — complete virtual filesystem semantics, process table, users,
and the deterministic fast-path for the whole command set — is implemented in
Weeks 2-3. Search for `TODO(week2)` / `TODO(week3)` markers.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StateSnapshot:
    """An immutable view of session state, injected into the LLM context."""

    cwd: str
    files_here: list[str]
    env: dict[str, str]
    last_exit_code: int

    def to_prompt_block(self) -> str:
        """Render the snapshot as a compact block for the system prompt."""
        files = " ".join(sorted(self.files_here)) or "(empty)"
        env = ", ".join(f"{k}={v}" for k, v in sorted(self.env.items())) or "(none)"
        return (
            "## CURRENT SESSION STATE (authoritative — never contradict this)\n"
            f"cwd: {self.cwd}\n"
            f"files in cwd: {files}\n"
            f"env: {env}\n"
            f"last exit code ($?): {self.last_exit_code}\n"
        )


class StateEngine:
    """Tracks the authoritative state of one attacker session.

    Deterministic commands mutate this state and can be answered directly
    (the "fast path"), keeping the honeypot consistent and reducing LLM calls.
    """

    def __init__(self) -> None:
        # Minimal virtual filesystem: {absolute_dir: set(child_names)}.
        # TODO(week2): replace with a proper inode-like VFS (files vs dirs,
        # contents, permissions, timestamps) supporting rm -r, mv, cp, etc.
        self._fs: dict[str, set[str]] = {"/": {"tmp", "var", "etc", "home"}}
        for d in ("/tmp", "/var", "/etc", "/home"):
            self._fs.setdefault(d, set())
        self.cwd: str = "/root"
        self._fs.setdefault("/root", set())
        self.env: dict[str, str] = {"HOME": "/root", "USER": "root", "PWD": "/root"}
        self.last_exit_code: int = 0

    # --- snapshot --------------------------------------------------------
    def snapshot(self) -> StateSnapshot:
        return StateSnapshot(
            cwd=self.cwd,
            files_here=sorted(self._fs.get(self.cwd, set())),
            env=dict(self.env),
            last_exit_code=self.last_exit_code,
        )

    # --- deterministic fast-path ----------------------------------------
    def try_fast_path(self, command: str) -> str | None:
        """Resolve a deterministic command from state, or return None.

        Returning None means "defer to the LLM". This skeleton handles a few
        commands so the demo is meaningful; the full set lands in Weeks 2-3.
        TODO(week3): export/echo $VAR, whoami, $?, ls <known path>, process cmds.
        """
        parts = command.strip().split()
        if not parts:
            self.last_exit_code = 0
            return ""
        cmd, args = parts[0], parts[1:]

        if cmd == "pwd":
            self.last_exit_code = 0
            return self.cwd

        if cmd == "cd":
            target = self._resolve(args[0]) if args else self.env["HOME"]
            if target in self._fs:
                self.cwd = target
                self.env["PWD"] = target
                self.last_exit_code = 0
                return ""
            self.last_exit_code = 1
            return f"bash: cd: {args[0]}: No such file or directory"

        if cmd == "mkdir" and args:
            target = self._resolve(args[-1])
            parent, name = self._split(target)
            self._fs.setdefault(parent, set()).add(name)
            self._fs.setdefault(target, set())
            self.last_exit_code = 0
            return ""

        if cmd == "ls" and not args:
            self.last_exit_code = 0
            return "  ".join(sorted(self._fs.get(self.cwd, set())))

        # Not a deterministic command we own yet → let the LLM handle it.
        return None

    # --- helpers ---------------------------------------------------------
    def _resolve(self, path: str) -> str:
        if path.startswith("/"):
            norm = path.rstrip("/")
            return norm or "/"
        joined = (self.cwd.rstrip("/") + "/" + path).rstrip("/")
        return joined or "/"

    @staticmethod
    def _split(abspath: str) -> tuple[str, str]:
        parent = abspath.rsplit("/", 1)[0] or "/"
        name = abspath.rsplit("/", 1)[-1]
        return parent, name
