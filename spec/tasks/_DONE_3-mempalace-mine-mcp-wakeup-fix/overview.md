# 3: MemPalace mine MCP — agent ignore + Windows wake-up stdout encoding

## Source seed
- Path: none

## Status
- [x] Spec created
- [x] Self spec review passed
- [x] Spec review passed
- [x] Code implemented
- [x] Self code review passed
- [x] Code review passed
- [x] Design documents updated

## Goal
Register the shipped mine MCP bridge in extension `agent-ignore` so agents skip it, and stop the post-mine `wake-up` subprocess from failing on Windows when captured stdout uses a legacy ANSI code page and MemPalace prints non-ASCII palace text.

## Design overview
- Affected modules: `extsrc/config.yaml` (`agent-ignore`); `extsrc/files/.mempalace/ext/mine_mcp_server.py` (subprocess environment for `mine` and `wake-up`).
- Data flow changes: After a successful `mempalace mine`, `_wake_up_write_wakeup_md` runs `mempalace wake-up` with `capture_output=True`. The child must not crash while encoding Unicode to the pipe; `.mempalace/wakeup.md` is only written when the wake-up process exits zero and returns decodable stdout.
- Integration points: Spawn extension `agent-ignore` merge in consumer workspaces; MemPalace CLI unchanged in this repo (fix is localized to the bridge script).

## Before → After
### Before
- `mine_mcp_server.py` is not listed under `agent-ignore`; agents may ingest it unnecessarily.
- On Windows, `subprocess.run(..., capture_output=True, text=True)` for `wake-up` uses the child interpreter’s narrow stdout encoding (often `cp1252`). MemPalace `cmd_wakeup` prints palace text containing characters such as U+2192 (`→`), raising `UnicodeEncodeError` inside the child; non-zero exit prevents writing UTF-8 `wakeup.md`, leaving a stale stub.

### After
- `mine_mcp_server.py` is covered by an explicit `agent-ignore` glob consistent with other paths.
- Mine and wake-up subprocess invocations use an augmented child env (e.g. `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8` as appropriate) so the child encodes Unicode to the pipe as UTF-8 on Windows, avoiding encode failures; the bridge decodes with `encoding="utf-8"` / `errors="replace"` so MCP payloads stay consistent; `wakeup.md` updates when wake-up succeeds.

## Details
- **Root cause (observed):** Failure occurs during child print/encode to the pipe, not during `Path.write_text` of `wakeup.md`. stderr may contain `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'`.
- **Scope:** Implement in `mine_mcp_server.py` only (this extension’s bridge). Upstream MemPalace CLI may still benefit from similar hardening; out of scope unless we add a cross-link in extension docs later.
- **Both subprocess sites:** Apply the same env helper to `_wake_up_write_wakeup_md` and `_tool_mempalace_mine` so `mine` stdout/stderr capture does not hit the same class of bug on exotic locales.
- **Env scope:** UTF-8-related variables apply only to the copied env passed into `subprocess.run` for MemPalace children, not to the MCP server process itself.
- **Risk:** Forcing UTF-8 mode in the MemPalace child could affect niche Windows path/console assumptions in upstream CLI; acceptable tradeoff for this bridge; if regressions appear, narrow to `PYTHONIOENCODING=utf-8` without `PYTHONUTF8` and retest.
- **agent-ignore pattern:** Use a repo-relative-style glob aligned with `spawn-ext-config` / packaged paths, e.g. `**/.mempalace/ext/mine_mcp_server.py`, appended to existing `agent-ignore` entries.
- **Verification:** Manual or scripted check on Windows: run `mempalace_mine` (or direct `wake-up` via the same subprocess helper) against a palace whose wake-up text includes arrows or other non-ASCII; expect `wakeup_written: true` and UTF-8 file content without encode traceback.

## Execution Scheme
> Each step id is the subtask filename (e.g. `1-abstractions`).
> MANDATORY! Each step is executed by a dedicated subagent (Task tool). Do NOT implement inline. No exceptions — even if a step seems trivial or small.
- Phase 1 (sequential): step `_DONE_1-agent-ignore-mine-mcp-server` → step `_DONE_2-subprocess-utf8-env-bridge`
