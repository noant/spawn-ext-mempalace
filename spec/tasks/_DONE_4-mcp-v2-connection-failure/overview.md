# 4: Fix primary MCP transport (wrong `mempalace mcp` CLI vs stdio server)

## Source seed
- Path: none

## Status
- [V] Spec created
- [V] Self spec review passed
- [V] Spec review passed
- [V] Code implemented
- [V] Self code review passed
- [V] Code review passed
- [V] Design documents updated

## Goal
Merge a primary **`mempalace-mcp`** stdio definition that launches **`mempalace.mcp_server`**, not the **`mcp`** CLI subcommand that only prints setup text and exits, so Cursor MCP V2 can complete the JSON-RPC handshake.

## Design overview
- Affected modules: **`extsrc/mcp/windows.json`**, **`linux.json`**, **`macos.json`** (`args` for **`mempalace-mcp`** only — mine server unchanged); **`extsrc/files/.mempalace/guides/guide.md`** (table row + checklist line that wrongly describe **`python -m mempalace mcp`** as the server); optional one-line tightening in **`extsrc/skills/mempalace-diagnose-palace.md`** under MCP; Step 7 update **`spec/design/hla.md`** (repository-role sentence still claims **`python -m mempalace mcp`** drives the primary server).
- Data flow changes: host spawns **`python` / `python3 -m mempalace.mcp_server`** → MemPalace reads **`MEMPALACE_PALACE_PATH`** as today → MCP JSON-RPC on restored real stdout after the module’s internal stdio protection.
- Integration points: Spawn MCP merge, Cursor MCP V2 stdio adapter, upstream **`mempalace`** package (**`cli.cmd_mcp`** vs **`mempalace.mcp_server:main`**, **`mempalace-mcp`** console entry when on PATH).

## Before → After
### Before
- Pack defaults **`args`: `["-m", "mempalace", "mcp"]`**, which invokes **`cli.cmd_mcp`**: prints human instructions to stdout and exits with code **0**. The MCP client expects JSON-RPC messages on stdout → immediate protocol failure (**`-32000: Connection closed`**, tools never appear).
- **`guide.md`** and **`spec/design/hla.md`** repeat the incorrect claim that this invocation is “the MCP server”.
### After
- Primary server **`args`**: **`["-m", "mempalace.mcp_server"]`** (same **`command`** per platform — **`python`** on Windows, **`python3`** on Linux/macOS) so stdin stays open for the protocol loop regardless of **`mempalace-mcp`** being on **`PATH`**.
- Documentation states **`mempalace mcp` / `python -m mempalace mcp`** as CLI *setup help only*, and points integrators at **`mempalace.mcp_server`** (or **`mempalace-mcp`** when shim is guaranteed).

## Details
### Root cause (validated)
Upstream MemPalace **3.x** registers **`mempalace-mcp = mempalace.mcp_server:main`**; the **`mcp`** subparser in **`cli.py`** only runs **`cmd_mcp`** (printed setup). There is **no** stdio server behind **`python -m mempalace mcp`**.
### Rationale for module form
Using **`python -m mempalace.mcp_server`** matches the historical pack goal (“no **`Scripts`** shim required on **`PATH`”) whereas relying on **`mempalace-mcp`** alone fails common user installs (**`shutil.which("mempalace-mcp")`** is **`None`** when Scripts is not on PATH).
### Mine server
**`mempalace-mine-mcp`** and **`.mempalace/ext/mine_mcp_server.py`** stay as-is unless a review finds conflicting assumptions.
### Versioning
Bump **`extsrc/config.yaml`** patch version when releasing this pack (per **`spawn-ext-increment-version`** convention); executor records final version during implementation.

### Constraints
- No code changes under **`spec/`** beyond this task folder until user Step 3 approval (**`spec/main.md`**).
- Do not widen scope (Chroma mining bridge, wakeup flow) beyond doc touch-ups needed for MCP accuracy.

### Verification (implementation phase)
- From a consumer repo root with **`mempalace`** installed for the IDE’s **`python`**: merged config shows **`python … -m mempalace.mcp_server`** — Cursor lists MemPalace tools on **`mempalace-mcp`** without **`Connection closed`** on connect.
- Optional shell smoke: **`python -m mempalace.mcp_server`** process remains alive waiting on stdin (**no immediate exit**).

## Execution Scheme
> Each step id is the subtask filename (e.g. `1-abstractions`).
> MANDATORY! Each step is executed by a dedicated subagent (Task tool). Do NOT implement inline. No exceptions — even if a step seems trivial or small.
- Phase 1 (sequential): step **`_DONE_1-fix-primary-mcp-json.md`** → step **`_DONE_2-align-pack-documentation.md`**
