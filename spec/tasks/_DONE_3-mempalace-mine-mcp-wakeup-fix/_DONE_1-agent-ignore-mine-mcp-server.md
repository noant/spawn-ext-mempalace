# 1-agent-ignore-mine-mcp-server

## Goal
Add the shipped mine MCP bridge script to Spawn extension `agent-ignore` so workspace agents do not unnecessarily index or surface it.

## Approach
- Extend `agent-ignore` in `extsrc/config.yaml` with a single glob that matches `mine_mcp_server.py` under `.mempalace/ext/` in consumer repos (consistent with the existing `files:` key `.mempalace/ext/mine_mcp_server.py`).
- Run `spawn extension check . --strict` after the edit if available in the environment; fix any schema complaints.

## Affected files
- `extsrc/config.yaml`

## Code examples
```yaml
agent-ignore:
  - "**/.mempalace/chroma/**"
  - "**/.mempalace/ext/mine_mcp_server.py"
```
