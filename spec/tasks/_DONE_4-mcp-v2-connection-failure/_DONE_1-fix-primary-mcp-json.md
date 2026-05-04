# 1: Fix primary MCP JSON (all platforms)

## Goal
Replace the **`mempalace-mcp`** transport **`args`** in every **`extsrc/mcp/*.json`** so Spawn merges a command that starts the real stdio server module.

## Approach
- Edit **`windows.json`**, **`linux.json`**, **`macos.json`** consistently: **`"args": ["-m", "mempalace.mcp_server"]`** for the server named **`mempalace-mcp`** only.
- Preserve **`command`**, **`cwd`**, **`env`**, **`capabilities`**, and the **`mempalace-mine-mcp`** server block verbatim unless a typo is discovered.
- Do not switch to **`mempalace-mcp`** as **`command`** unless a follow-on task deliberately standardizes PATH — this step stays with **`python` / `python3` + `-m`** for reproducibility across installs.

## Affected files
- **`extsrc/mcp/windows.json`**
- **`extsrc/mcp/linux.json`**
- **`extsrc/mcp/macos.json`**

## Code examples (exact target shape — illustrative)

```json
"args": ["-m", "mempalace.mcp_server"]
```

## Deliverables
Valid JSON committed; merged primary server invokes **`mempalace.mcp_server`**.
