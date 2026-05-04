# 2: Guides, README, HLA, diagnose — `extsrc/mcp/` wording

## Goal
Update prose that referenced **`extsrc/mcp.json`** to describe **`extsrc/mcp/*.json`**, OS selection, and **`python`** vs **`python3`** defaults plus adapter overrides.

## Affected files
- `extsrc/files/.mempalace/guides/guide.md`
- `README.md`
- `spec/design/hla.md`
- `extsrc/skills/mempalace-diagnose-palace.md` (if MCP/palace bullets still mention bare **`mempalace mcp`** only)

## Verification
- No stale **`extsrc/mcp.json`** references in shipped pack docs; troubleshooting mentions per-platform merge.
