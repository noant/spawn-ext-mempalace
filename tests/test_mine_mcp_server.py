"""Tests for ``.mempalace/ext/mine_mcp_server.py`` (MCP bridge for ``mempalace mine``)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_tool_schema_only_core_parameters(mine_mod):
    props = mine_mod.TOOLS["mempalace_mine"]["input_schema"]["properties"]
    assert set(props.keys()) == {"directory", "mode", "wing", "palace"}


def test_initialize_returns_server_info(mine_mod):
    req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}}
    resp = mine_mod._handle_request(req)
    assert resp["id"] == 1
    assert resp["result"]["serverInfo"]["name"] == "mempalace-mine-mcp"
    assert resp["result"]["protocolVersion"] == "2024-11-05"


def test_tools_list_exposes_mempalace_mine(mine_mod):
    req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    resp = mine_mod._handle_request(req)
    names = [t["name"] for t in resp["result"]["tools"]]
    assert names == ["mempalace_mine"]
    mine = resp["result"]["tools"][0]
    assert set(mine["inputSchema"]["properties"].keys()) == {"directory", "mode", "wing", "palace"}


def test_mine_projects_command_minimal(monkeypatch, mine_mod, tmp_path: Path):
    (tmp_path / "proj").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", raising=False)

    captured: dict = {"cmds": []}

    def fake_run(cmd, **kwargs):
        captured["cmds"].append(list(cmd))
        captured["cwd"] = kwargs.get("cwd")
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "done\n", "")
        if "wake-up" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "## wake\nfresh\n", "")
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    out = mine_mod._tool_mempalace_mine(directory="proj", mode="projects")
    assert out["exit_code"] == 0
    assert out["stdout"] == "done"
    assert out.get("wakeup_written") is True
    wakeup = tmp_path / ".mempalace" / "wakeup.md"
    assert wakeup.read_text(encoding="utf-8") == "## wake\nfresh\n"

    cmd = captured["cmds"][0]
    assert cmd[0] == "/bin/mempalace"
    assert cmd[1:3] == ["--palace", str((tmp_path / ".mempalace" / "palace").resolve())]
    assert cmd[3] == "mine"
    assert cmd[4] == str((tmp_path / "proj").resolve())
    assert "--mode" not in cmd
    assert "--dry-run" not in cmd
    assert "--limit" not in cmd
    assert cmd[-2:] == ["--agent", "mcp"]


def test_mine_convos_adds_mode_and_extract(monkeypatch, mine_mod, tmp_path: Path):
    (tmp_path / "chats").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", raising=False)
    captured: dict = {"cmds": []}

    def fake_run(cmd, **kwargs):
        captured["cmds"].append(list(cmd))
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if "wake-up" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "ok", "")
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    mine_mod._tool_mempalace_mine(directory="chats", mode="convos")
    cmd = captured["cmds"][0]
    assert "--mode" in cmd and cmd[cmd.index("--mode") + 1] == "convos"
    assert "--extract" in cmd and cmd[cmd.index("--extract") + 1] == "exchange"


def test_mine_palace_and_wing(monkeypatch, mine_mod, tmp_path: Path):
    (tmp_path / "d").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", raising=False)
    captured: dict = {"cmds": []}

    def fake_run(cmd, **kwargs):
        captured["cmds"].append(list(cmd))
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if "wake-up" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    mine_mod._tool_mempalace_mine(
        directory="d",
        mode="projects",
        wing="mywing",
        palace="~/custom/palace",
    )
    cmd = captured["cmds"][0]
    i = cmd.index("--palace")
    assert cmd[i + 1].endswith("custom/palace") or "custom" in cmd[i + 1]
    assert "--wing" in cmd and cmd[cmd.index("--wing") + 1] == "mywing"
    wake = captured["cmds"][1]
    assert "wake-up" in wake
    assert "--palace" in wake
    wi = wake.index("--wing")
    assert wake[wi + 1] == "mywing"


def test_mine_failure_skips_wakeup(monkeypatch, mine_mod, tmp_path: Path):
    (tmp_path / "p").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", raising=False)
    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(list(cmd))
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 1, "", "mine failed")
        return subprocess.CompletedProcess(cmd, 0, "no", "")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    out = mine_mod._tool_mempalace_mine(directory="p", mode="projects")
    assert out["exit_code"] == 1
    assert "wakeup_written" not in out
    assert len(calls) == 1
    assert not (tmp_path / ".mempalace").exists()


def test_mine_missing_directory_returns_error(monkeypatch, mine_mod, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    out = mine_mod._tool_mempalace_mine(directory="does-not-exist")
    assert "error" in out
    assert "not a directory" in out["error"]


def test_tools_call_strips_unknown_arguments(monkeypatch, mine_mod, tmp_path: Path):
    (tmp_path / "x").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", raising=False)

    def fake_run(cmd, **kwargs):
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if "wake-up" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    req = {
        "jsonrpc": "2.0",
        "id": 9,
        "method": "tools/call",
        "params": {
            "name": "mempalace_mine",
            "arguments": {
                "directory": "x",
                "mode": "projects",
                "dry_run": True,
                "limit": 99,
            },
        },
    }
    resp = mine_mod._handle_request(req)
    assert "result" in resp
    text = resp["result"]["content"][0]["text"]
    payload = json.loads(text)
    assert payload.get("exit_code") == 0


def test_mine_uses_env_palace_when_set(monkeypatch, mine_mod, tmp_path: Path):
    ext = tmp_path / "outside_palace"
    ext.mkdir()
    (tmp_path / "p").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", raising=False)
    monkeypatch.setenv("MEMPALACE_PALACE_PATH", str(ext.resolve()))

    captured: dict = {"cmds": []}

    def fake_run(cmd, **kwargs):
        captured["cmds"].append(list(cmd))
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if "wake-up" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "ok", "")
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    mine_mod._tool_mempalace_mine(directory="p", mode="projects")
    mine_cmd = captured["cmds"][0]
    i = mine_cmd.index("--palace")
    assert mine_cmd[i + 1] == str(ext.resolve())


def test_mine_skips_explicit_palace_when_global_override(monkeypatch, mine_mod, tmp_path: Path):
    (tmp_path / "p").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    monkeypatch.delenv("MEMPAL_PALACE_PATH", raising=False)
    monkeypatch.setenv("MEMPALACE_EXTENSION_GLOBAL_PALACE", "1")

    captured: dict = {"cmds": []}

    def fake_run(cmd, **kwargs):
        captured["cmds"].append(list(cmd))
        if "mine" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if "wake-up" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mine_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(mine_mod, "_mempalace_cli", lambda: ["/bin/mempalace"])

    mine_mod._tool_mempalace_mine(directory="p", mode="projects")
    assert "--palace" not in captured["cmds"][0]
    assert "--palace" not in captured["cmds"][1]
