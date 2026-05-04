# 1: configure-palace skill — repo-local palace, slices, MCP UI

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
Tighten the **mempalace-configure-palace** skill text: repo-local palace only; a concrete flow for alternate organizational slices (propose folding them into config immediately and apply after user consent); and an explicit note to enable MCP in the IDE UI when needed.

## Design overview
- Affected modules: `extsrc/skills/mempalace-configure-palace.md`, and optionally one short paragraph in `extsrc/files/.mempalace/guides/guide.md` (**IDE wiring checklist**) if referencing the skill alone is insufficient for “see guide” cohesion.
- Data flow changes: none for data or runtime — only agent instruction wording and optionally user-facing guide text.
- Integration points: skills rendered from `config.yaml`; guides are merged as this pack’s required local reads.

## Before → After
### Before
- The skill describes **global** vs **local** mode as step one and alternate slices (domain / layer / lifecycle, etc.) mostly as comparison without a mandatory “draft YAML edits and ask for consent before patching” step.

### After
- For this extension pack, **only** a **repo-local** palace `<repo>/.mempalace/palace` with aligned `palace_path` / `MEMPALACE_PALACE_PATH` is canonical in this skill text; **do not steer** readers toward the global-memory path (upstream docs and `configuration.md` remain the factual sources for global config — no mandate to purge every mention elsewhere).
- After the topology sketch and **alternate slices**: the agent spells out each slice the user buys into as a **concrete file-level proposal** (`mempalace.yaml`: `rooms` / ordering, primary **`wing`** for default mining; extra `mempalace_mine` passes with **`wing` where CLI/UIs allow — see existing guides), **asks once** for confirmation, and on consent **edits** the listed workspace files (and reminds about re-`mine`/MCP reconnect when structure changes).
- The MCP-related section advises: if tools are missing after merging config, **check that MCP servers are enabled in the IDE** (exact panel wording depends on Cursor/VS Code lineage — phrase generically, not tied to a single build forever).

## Details
- **Stay within the configure skill (+ optional `guide.md`)**: do not edit the diagnose skill purely for symmetry if its wording still aligns after configure changes.
- **Upstream**: do not invent YAML keys; post-consent actions must match official configuration docs or patterns already established in this repo (skills reference `guide.md` and the configuration guide).
- **MCP UI phrasing**: “enable / turn on MCP servers in the IDE shell” without a brittle menu changelog; optionally mention merged config, reload, and tooling list anchor points.

## Execution Scheme
> Each step id is the subtask filename (e.g. `1-abstractions`).
> MANDATORY! Each step is executed by a dedicated subagent (Task tool). Do NOT implement inline. No exceptions — even if a step seems trivial or small.
- Phase 1 (sequential): step `_DONE_1-skill-local-slices-mcp-ui.md`
- Phase 2 (optional, sequential): step `_DONE_2-guide-ide-mcp-enable-hint.md` — run only if, after phase 1, a short skill pointer to **IDE wiring checklist** proves insufficient and a second reading anchor in `guide.md` is needed
