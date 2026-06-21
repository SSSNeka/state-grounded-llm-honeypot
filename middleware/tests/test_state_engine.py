from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from state_grounded import StateEngine  # noqa: E402


def test_initial_state_pwd() -> None:
    eng = StateEngine()
    assert eng.cwd == "/root"
    assert eng.try_fast_path("pwd") == "/root"


def test_mkdir_then_ls() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("mkdir /tmp/x") == ""
    assert eng.try_fast_path("ls /tmp") == "x"


def test_relative_paths() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("cd /tmp") == ""
    assert eng.try_fast_path("mkdir demo") == ""
    assert eng.try_fast_path("ls") == "demo"
    assert eng.try_fast_path("cd ..") == ""
    assert eng.try_fast_path("pwd") == "/"


def test_path_normalization() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("cd /tmp/../var") == ""
    assert eng.try_fast_path("pwd") == "/var"


def test_cd_failure_keeps_cwd_and_sets_exit_code() -> None:
    eng = StateEngine()
    out = eng.try_fast_path("cd /does-not-exist")
    assert out == "bash: cd: /does-not-exist: No such file or directory"
    assert eng.cwd == "/root"
    assert eng.last_exit_code == 1


def test_mkdir_duplicate_directory_fails() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("mkdir /tmp/x") == ""
    out = eng.try_fast_path("mkdir /tmp/x")
    assert out == "mkdir: cannot create directory '/tmp/x': File exists"
    assert eng.last_exit_code == 1


def test_mkdir_missing_parent_fails() -> None:
    eng = StateEngine()
    out = eng.try_fast_path("mkdir /missing/x")
    assert out == "mkdir: cannot create directory '/missing/x': No such file or directory"
    assert eng.last_exit_code == 1


def test_rm_directory_requires_recursive_flag() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("mkdir /tmp/demo") == ""
    out = eng.try_fast_path("rm /tmp/demo")
    assert out == "rm: cannot remove '/tmp/demo': Is a directory"
    assert eng.last_exit_code == 1
    assert eng.try_fast_path("rm -r /tmp/demo") == ""
    assert eng.try_fast_path("ls /tmp") == ""


def test_rm_recursive_root_is_rejected() -> None:
    eng = StateEngine()
    out = eng.try_fast_path("rm -r /")
    assert out == "rm: refusing to remove root directory '/'"
    assert eng.last_exit_code == 1


def test_rm_recursive_cwd_path_is_busy_and_cwd_is_preserved() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("cd /tmp") == ""
    out = eng.try_fast_path("rm -r /tmp")
    assert out == "rm: cannot remove '/tmp': Device or resource busy"
    assert eng.cwd == "/tmp"
    assert eng.last_exit_code == 1


def test_fast_path_contract() -> None:
    eng = StateEngine()
    for command in ("pwd", "cd /tmp", "mkdir /tmp/x", "ls /tmp", "rm -r /tmp/x"):
        assert eng.try_fast_path(command) is not None
    assert eng.try_fast_path("uname -a") is None


def test_malformed_quoted_command_returns_shell_error() -> None:
    eng = StateEngine()
    out = eng.try_fast_path('mkdir "unterminated')
    assert out is not None
    assert eng.last_exit_code == 1


def test_successful_pwd_resets_last_exit_code_after_failure() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("cd /does-not-exist") == (
        "bash: cd: /does-not-exist: No such file or directory"
    )
    assert eng.last_exit_code == 1
    assert eng.try_fast_path("pwd") == "/root"
    assert eng.last_exit_code == 0


def test_snapshot_tracks_cwd_and_direct_children() -> None:
    eng = StateEngine()
    eng.try_fast_path("cd /tmp")
    eng.try_fast_path("mkdir keep")
    eng.try_fast_path("mkdir remove")
    eng.try_fast_path("rm -r remove")
    snap = eng.snapshot()
    assert snap.cwd == "/tmp"
    assert snap.files_here == ["keep"]
    assert snap.env["PWD"] == "/tmp"
