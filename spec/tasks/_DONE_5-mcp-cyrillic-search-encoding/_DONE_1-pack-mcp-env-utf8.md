# Step 1: Pack MCP — UTF-8 stdio and Windows UTF-8 mode (as shipped)

## Goal
Ensure UTF-8 for MCP server processes: **PYTHONIOENCODING=utf-8** on all platforms; on Windows enable UTF-8 **mode** via interpreter flags, not **PYTHONUTF8** in **env**.

## As shipped
1. **windows.json** (both **mempalace-mcp** and **mempalace-mine-mcp**):
   - **env**: **PYTHONIOENCODING** = **utf-8**, existing **MEMPALACE_PALACE_PATH** placeholder unchanged.
   - **	ransport.args**: **py -3 -X utf8 -m mempalace.mcp_server** / **py -3 -X utf8 .mempalace/ext/mine_mcp_server.py**.
   - **No** **PYTHONUTF8** key in **env** (avoids **invalid PYTHONUTF8** when hosts merge malformed values).
2. **linux.json** / **macos.json**: **PYTHONIOENCODING=utf-8** in **env** for both servers only (**PYTHONUTF8** not added on Unix).
3. **spawn extension check . --strict**.

## Affected files
- **extsrc/mcp/windows.json**
- **extsrc/mcp/linux.json**
- **extsrc/mcp/macos.json**
