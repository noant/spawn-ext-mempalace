# 2-subprocess-utf8-env-bridge

## Goal
Prevent `UnicodeEncodeError` in the MemPalace child process when `mine_mcp_server.py` captures `mine` / `wake-up` stdout/stderr on Windows (narrow console/pipe encoding).

## Approach
- Introduce a small helper (e.g. `_subprocess_env_utf8()`) that copies `os.environ` and sets UTF-8 oriented variables for the Python child:
  - Prefer `PYTHONUTF8=1` (Python 3.7+ on Windows) and/or `PYTHONIOENCODING=utf-8` so `print()` and default TextIO encoding toward the pipe use UTF-8.
  - Apply on all platforms or gate on `sys.platform == "win32"` — either is acceptable if behavior stays safe on Unix (document choice in a one-line comment if non-obvious).
- Use this env for **both** `subprocess.run` calls: `_tool_mempalace_mine` (mine) and `_wake_up_write_wakeup_md` (wake-up).
- Keep `capture_output=True`, `text=True`. Address **child-side** encode failures with the env helper; **also** pass `encoding="utf-8"` and `errors="replace"` on both `subprocess.run` calls so the bridge decodes captured stdout/stderr consistently with UTF-8 bytes from the pipe (avoids mojibake in MCP tool payloads on Windows).

## Affected files
- `extsrc/files/.mempalace/ext/mine_mcp_server.py`

## Notes
- Do not change MCP protocol or tool schemas.
- Forcing UTF-8 in the MemPalace child is an acceptable tradeoff; if upstream regressions appear on Windows, try `PYTHONIOENCODING=utf-8` without `PYTHONUTF8` and retest.
- If bump policy applies after functional extension behavior change, treat as material consumer-facing fix — coordinate version bump per `spawn-ext-increment-version` after implementation (Step 4 / release hygiene).
