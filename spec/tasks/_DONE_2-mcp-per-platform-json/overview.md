# 2: MCP servers — per-platform `extsrc/mcp/*.json` + `python -m` launch

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
Ship bundled **`mempalace-mcp`** and **`mempalace-mine-mcp`** via Spawn’s **three-file** MCP layout (**`extsrc/mcp/windows.json`**, **`linux.json`**, **`macos.json`**) so each host OS gets a **`transport`** with the usual interpreter name (**`python`** on Windows, **`python3`** on Linux/macOS), and the primary server runs **without** a **`mempalace`** / **`Scripts`** shim on **`PATH`**.

## Design overview
- Affected modules: **`extsrc/mcp/*.json`** (replaces obsolete **`extsrc/mcp.json`**), **`extsrc/files/.mempalace/guides/guide.md`**, **`extsrc/skills/mempalace-diagnose-palace.md`**, root **`README.md`**, **`spec/design/hla.md`**.
- Data flow: unchanged **`cwd`** + **`MEMPALACE_PALACE_PATH`**; **`mempalace-mcp`** uses **`python(3) -m mempalace mcp`**; the mine bridge uses the same **`command`** as in that platform file.
- Integration points: Spawn selects one JSON per host OS; identical **`servers[].name`** sets across all three files.

## Before → After
### Before
- Single obsolete **`extsrc/mcp.json`** with bare **`mempalace`** **`command`** → Windows **`'mempalace' is not recognized`**, and no first-class per-OS **`python`** vs **`python3`**.

### After
- **`extsrc/mcp/*.json`** with aligned **`name`** sets; Windows **`python`**, Linux/macOS **`python3`**; primary server uses **`-m mempalace mcp`** (pinned **`mempalace==3.3.4`**). Docs and **`spec/design/hla.md`** describe **`extsrc/mcp/`**.

## Details
- **Removed:** **`extsrc/mcp.json`** — **`spawn extension check`** flags it if reintroduced.
- **Version:** **`extsrc/config.yaml`** bumped for the MCP contract change (**`0.2.21`**).

## Execution Scheme
> Each step id is the subtask filename.
- Phase 1 (sequential): step `_DONE_1-mcp-json-primary-transport.md` → step `_DONE_2-docs-and-skills-alignment.md`
