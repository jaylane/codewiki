"""Shared fixtures."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    def run(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)
    run("init", "-q")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "test")
    run("config", "commit.gpgsign", "false")
    run("commit", "--allow-empty", "-m", "init")
    return tmp_path
