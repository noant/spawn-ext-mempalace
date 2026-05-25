# 6: Bump pinned MemPalace PyPI release

## Source seed
- Path: none

## Status
- [V] Spec created
- [V] Self spec review passed
- [V] Spec review passed
- [V] Code implemented
- [V] Self code review passed
- [V] Code review passed
- [V] Design documents updated

## Goal
Adopt the latest published **`mempalace`** on PyPI (**3.3.5**) in the extension install hook and mirrored requirements file, and bump the pack **`version`** for release.

## Design overview
- Affected modules: **`extsrc/setup/after_install.py`** (`MEMPALACE_PYPI_VERSION`); **`extsrc/files/.mempalace/ext/requirements-mempalace.txt`**; **`extsrc/config.yaml`** (`version`).
- Data flow changes: **`spawn extension add` / `update`** and manual **`pip install -r .mempalace/ext/requirements-mempalace.txt`** install **3.3.5** instead of **3.3.4**. No MCP transport or server-name changes.
- Integration points: PyPI **`https://pypi.org/pypi/mempalace/json`** (authoritative latest **`info.version`**); **`spawn extension check . --strict`**; optional **`spawn extension healthcheck mempalace`** in a disposable target (per **`spawn-ext-verify`**).

## Before → After
### Before
- **`MEMPALACE_PYPI_VERSION`** and **`requirements-mempalace.txt`** pin **`mempalace==3.3.4`**.
- Extension pack **`version`**: **`0.3.1`**.

### After
- Both pins: **`mempalace==3.3.5`** (matches PyPI latest as of spec date **2026-05-25**).
- Extension pack **`version`**: **`0.3.2`** (patch — consumer-visible dependency pin change).

## Details
- **Discovery (done for spec):** PyPI JSON reports **`3.3.5`** as current release (upload **2026-05-10**); prior pin **3.3.4**. At implementation (Step 4), re-fetch **`https://pypi.org/pypi/mempalace/json`** once; if **`info.version`** is newer than **3.3.5**, use that instead and note it in the PR/commit message.
- **Scope:** Patch-level upstream bump only — do **not** change **`extsrc/mcp/*.json`**, skills, or **`mine_mcp_server.py`** unless strict check or smoke test reveals a required follow-up (out of scope unless blocking).
- **Sync rule:** Comment in **`requirements-mempalace.txt`** already requires parity with **`after_install.py`** — update **both** in one step.
- **Docs:** **`README.md`** and guides refer to “pinned” generically; no hardcoded **3.3.4** outside historical **`_DONE_`** tasks — no doc edits unless executor finds a stale literal.
- **HLA:** No architectural change; Step 7 may skip **`spec/design/hla.md`** unless maintainer wants the pin called out (optional one-line note).

## Execution Scheme
> Each step id is the subtask filename (e.g. `1-abstractions`).
> MANDATORY! Each step is executed by a dedicated subagent (Task tool). Do NOT implement inline. No exceptions — even if a step seems trivial or small.
- Phase 1 (sequential): step `1-update-pypi-pins` → step `2-bump-pack-version-and-verify`
