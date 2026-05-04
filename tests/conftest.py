"""Pytest fixtures: load ``mine_mcp_server`` from extension source (outside Spawn ``extsrc`` install)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MINE_SERVER_PATH = REPO_ROOT / "extsrc" / "files" / ".mempalace" / "ext" / "mine_mcp_server.py"


@pytest.fixture(scope="module")
def mine_mod():
    assert MINE_SERVER_PATH.is_file(), f"missing {MINE_SERVER_PATH}"
    spec = importlib.util.spec_from_file_location("_mine_mcp_server_under_test", MINE_SERVER_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod
