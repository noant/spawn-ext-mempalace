"""Tests for ``extsrc/setup/healthcheck.py``."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HEALTHCHECK_PATH = REPO_ROOT / "extsrc" / "setup" / "healthcheck.py"


@pytest.fixture(scope="module")
def healthcheck_mod():
    assert HEALTHCHECK_PATH.is_file(), f"missing {HEALTHCHECK_PATH}"
    spec = importlib.util.spec_from_file_location("_healthcheck_under_test", HEALTHCHECK_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def test_healthcheck_passes_when_chroma_imports(healthcheck_mod):
    pytest.importorskip("mempalace")
    assert healthcheck_mod.main() == 0


def test_healthcheck_message_mentions_attrs_and_requirements(healthcheck_mod, monkeypatch, capsys):
    pytest.importorskip("mempalace")

    real_import = __import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "mempalace.backends" and fromlist and "chroma" in fromlist:
            raise ImportError("No module named 'attrs'")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr("builtins.__import__", fake_import)

    rc = healthcheck_mod.main()
    captured = capsys.readouterr()
    assert rc == 1
    assert "attrs>=22.2.0" in captured.out
    assert "requirements-mempalace.txt" in captured.out
    assert "Chroma deps" in captured.out
