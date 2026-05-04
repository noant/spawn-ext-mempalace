# 1 — Skill: repo-local palace, slices with apply path, MCP UI

## Goal
Align `extsrc/skills/mempalace-configure-palace.md` with the task specification in `overview.md`.

## Approach
1. Remove or replace the **modes** bullet so **“single global palace” is never offered as part of this skill**: describe only the **repo-local** palace and alignment with the pack MCP `env`, with a minimal pointer to `guide.md`/configuration for edge cases — no second UX path centered on global MemPalace storage.
2. Rewrite **Alternate cuts**: after comparing slices, add an explicit workflow — surface a **change draft** to the user (which `rooms`/`wing`/mining plan), one confirmation question for applying it, then **write the files** on approval and remind about **`mine`** when structure changes.
3. Add guidance on **enabling MCP in the IDE shell** wherever the skill talks about servers/tools (before or after the `guide.md` pointer): merged config alone may not suffice — confirm MCP servers are **enabled** in the client settings and reload if necessary.

## Affected files
- `extsrc/skills/mempalace-configure-palace.md`

## Examples / constraints (illustrative)
- Avoid “mode A / mode B” branching that sells a global path; phrase like “this skill covers **repository** wiring under `.mempalace/palace`”.
- For slices: move from “offer two alternate views” to **concrete YAML deltas + consent + apply**.
