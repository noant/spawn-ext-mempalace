# 2: Align pack documentation with real MCP entrypoint

## Goal
Remove false statements that **`python -m mempalace mcp`** (or **`mempalace mcp`**) runs the MCP stdio server; document the CLI subcommand as setup help only and the merged default as **`mempalace.mcp_server`**.

## Approach
1. **`extsrc/files/.mempalace/guides/guide.md`**
   - Fix the MCP table row for **`mempalace-mcp`**: describe **`python`** / **`python3 -m mempalace.mcp_server`** per platform defaults (keep note that operators may override **`command`** / **`args`**).
   - Fix the checklist sentence that treats **`python -m mempalace.mcp_server`** as secondary to **`python -m mempalace mcp`** — invert: primary merged default is the **module**, **`mcp`** subcommand remains optional human-facing setup text.
   - Mention briefly that **`mempalace mcp`** prints setup instructions only (upstream CLI behavior).

2. **`extsrc/skills/mempalace-diagnose-palace.md`**
   - Under **MCP**, add one explicit diagnostic cue: failure with immediate disconnect / no tools → verify the merged primary server targets **`mempalace.mcp_server`**, not **`mcp`**.

3. **Step 7 (design docs)** — not done in Step 4; executor updates **`spec/design/hla.md`** repository-role line to **`python -m mempalace.mcp_server`** (and **`python3`** wording for Unix).

4. Repo-wide skim under **`extsrc/`** only for lingering **`"-m mempalace mcp"`** or “same behavior as **`mempalace mcp`** MCP” claims; fix if found without expanding scope beyond this task.

## Affected files (implementation phase)
- **`extsrc/files/.mempalace/guides/guide.md`**
- **`extsrc/skills/mempalace-diagnose-palace.md`** (minimal delta)
- **`spec/design/hla.md`** (Step 7)

## Verification
Prose matches merged JSON after step 1; no remaining claim that **`mempalace mcp`** launches the MCP protocol.
