# 7: Fix `mempalace mine` / mine MCP — missing or stale `attrs` transitive dep

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
Ensure Spawn extension installs satisfy the `chromadb → jsonschema → attrs` chain so `mempalace mine` and **`mempalace-mine-mcp`** succeed, and fail early with an actionable healthcheck when they do not.

## Design overview
- Affected modules: **`extsrc/files/.mempalace/ext/requirements-mempalace.txt`**; **`extsrc/setup/after_install.py`** (pip install step); **`extsrc/setup/healthcheck.py`**; **`extsrc/skills/mempalace-diagnose-palace.md`** (troubleshooting); optional **`tests/`** for healthcheck.
- Data flow changes: **`after_install`** / manual **`pip install -r .mempalace/ext/requirements-mempalace.txt`** install **`attrs>=22.2.0`** alongside pinned **`mempalace`**. **`spawn extension healthcheck mempalace`** validates the same import path **`mempalace mine`** uses (Chroma backend), not only top-level **`import mempalace`**. Mine MCP bridge unchanged — it already surfaces subprocess stderr.
- Integration points: consumer Python env (often **`py -3`** on Windows per **`extsrc/mcp/windows.json`**); PyPI **`mempalace`**, **`chromadb`**, **`jsonschema`**, **`attrs`**; upstream MemPalace lazy-imports Chroma in **`miner`**, not at package root.

## Before → After
### Before
- **`requirements-mempalace.txt`** lists only **`mempalace==3.3.5`**.
- **`after_install.py`** runs **`pip install mempalace==3.3.5`** (single spec). Pip may leave a pre-existing incompatible **`attrs`** (e.g. **18.2.0** pulled by **`pdflatex`**) that satisfies no resolver conflict but breaks **`jsonschema 4.x`** (`from attrs import define` → **`ModuleNotFoundError: No module named 'attrs'`** or **`pip check`** warnings).
- **`healthcheck.py`** only **`import mempalace`** — passes while **`mempalace mine`** / **`from mempalace.miner import mine`** fails on Chroma import.
- **`mempalace_mine`** returns **`exit_code: 1`** with the traceback shown in the user report.

### After
- **`requirements-mempalace.txt`** pins **`mempalace==3.3.5`** and **`attrs>=22.2.0`** (comment explains jsonschema/Chroma requirement).
- **`after_install.py`** installs from the shipped requirements file (or equivalent multi-spec install with **`attrs>=22.2.0`**) so fresh extension add/update upgrades **`attrs`** when needed.
- **`healthcheck.py`** imports **`mempalace.backends.chroma`** (or **`from mempalace.miner import mine`**) and prints a clear fix hint (**re-run pip install from requirements**) on failure.
- **`mempalace-diagnose-palace`** skill documents this failure mode and one-line recovery for existing broken envs.

## Details
### Root cause (reproduced on maintainer Python 3.14, 2026-05-25)
Observed chain when **`mempalace_mine`** runs **`mempalace mine`**:

```
mempalace.cli cmd_mine → miner → palace → backends.chroma → chromadb
→ jsonschema → from attrs import define → ModuleNotFoundError: No module named 'attrs'
```

Contributing factors:
1. **`jsonschema>=4.19`** (Chroma dep) requires **`attrs>=22.2.0`**.
2. User site-packages may already contain **`attrs 18.2.0`** (e.g. **`pdflatex`** constraint **`attrs<19`**) — metadata present, module not importable as modern **`attrs`**, and pip does not upgrade it when only **`mempalace`** is installed.
3. **`import mempalace`** succeeds; Chroma/miner imports are lazy — current healthcheck is insufficient.

**Immediate user workaround (until extension update is installed):**

```bash
pip install "attrs>=22.2.0"
# or, after this task ships:
pip install -r .mempalace/ext/requirements-mempalace.txt
```

Verified locally: upgrading **`attrs`** to **26.1.0** fixes **`from mempalace.miner import mine`**.

### Fix options considered
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Pin **`attrs>=22.2.0`** in extension requirements + after_install | Extension-controlled; fixes fresh installs and re-installs; minimal diff | Does not auto-fix envs that never re-run pip; may conflict with **`pdflatex`** if both used in same interpreter | **Adopt** |
| Upstream MemPalace declares **`attrs>=22.2.0`** in **`pyproject.toml`** | Correct ownership | Out of scope for this repo; extension still needs pin until users upgrade MemPalace | Note for upstream; extension pin anyway |
| Healthcheck + diagnose docs only | Fast | Does not prevent broken installs | **Combine** with pin |
| Lazy-import / optional Chroma in MemPalace | Avoids import at mine time | Upstream architectural change | Reject |

### Scope boundaries
- Do **not** change **`extsrc/mcp/*.json`** transport (failure is deps, not MCP wiring).
- Do **not** bump **`mempalace`** PyPI pin unless strict verify reveals a required upstream release (unlikely for this bug).
- **`pdflatex` / attrs<19** conflict: document in diagnose skill; do not add **`pdflatex`** to extension requirements. If both tools must coexist, user needs separate venvs — mention briefly.

### Verification (Step 4)
1. In a disposable venv: pre-install **`attrs==18.2.0`**, run extension install path (requirements + after_install logic), assert **`from mempalace.miner import mine`** succeeds.
2. **`spawn extension healthcheck mempalace`** exits 0 after fix, 1 with actionable message before fix.
3. Optional: **`pytest tests/`** if healthcheck tests are added.

## Execution Scheme
> Each step id is the subtask filename (e.g. `1-abstractions`).
> MANDATORY! Each step is executed by a dedicated subagent (Task tool). Do NOT implement inline. No exceptions — even if a step seems trivial or small.
- Phase 1 (sequential): step `_DONE_1-pin-attrs-requirements-after-install` → step `_DONE_2-healthcheck-chromadb-import-chain` → step `_DONE_3-diagnose-skill-attrs-troubleshooting`
