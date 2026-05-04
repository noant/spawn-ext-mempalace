# 1: Primary MCP — `extsrc/mcp/*.json` + platform `command`

## Goal
Replace obsolete **`extsrc/mcp.json`** with **`extsrc/mcp/windows.json`**, **`linux.json`**, and **`macos.json`**. Use **`python -m mempalace mcp`** for **`mempalace-mcp`**; set **`command`** to **`python`** on Windows and **`python3`** on Linux/macOS for **both** servers. Keep identical **`servers[].name`** sets across files.

## Approach
1. Add the three JSON files; delete **`extsrc/mcp.json`**.
2. Bump **`extsrc/config.yaml`** **`version`** (MCP behavior change).
3. Run **`spawn extension check .`** (`--strict` in CI if applicable).

## Affected files
- `extsrc/mcp/windows.json`, `extsrc/mcp/linux.json`, `extsrc/mcp/macos.json`
- (removed) `extsrc/mcp.json`
- `extsrc/config.yaml`

## Verification
- **`python -m mempalace mcp`** works for **`mempalace==3.3.4`** on the target interpreter.
- Check reports no obsolete **`mcp.json`** and matching server **`name`** sets.
