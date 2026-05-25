# High-Level Architecture (HLA)

## Repository role

This repository is a **Spawn extension** (**`extsrc/`**, pack **`0.3.3`**) that installs MemPalace scaffolding into consumer repos: **`after_install.py`** installs pinned deps from **`.mempalace/ext/requirements-mempalace.txt`** (**`mempalace==3.3.5`**, **`attrs>=22.2.0`** for the Chroma/jsonschema chain) and drives **`mempalace init`**, templated **`extsrc/files/.mempalace/**`** (guides, MCP bridge stub, wakeup artifact hook), **`extsrc/mcp/{windows,linux,macos}.json`** merge two stdio MCP servers per host OS with **`MEMPALACE_PALACE_PATH=.mempalace/palace`** (primary server via **`python -m mempalace.mcp_server`** on Windows; **`python3 -m mempalace.mcp_server`** on Linux/macOS in pack defaults), and **`extsrc/skills/*.md`** are rendered per **`config.yaml`**. **`healthcheck.py`** verifies **`mempalace.backends.chroma`** import (same path as **`mempalace mine`**), not only top-level **`import mempalace`**.

## Runtime and data flows

Palace vectors and CLI state live **under each target repo** (default **`.mempalace/palace`** aligned with MCP env); global MemPalace config remains documented upstream and in **`configuration.md`**, not as the primary path in the **`mempalace-configure-palace`** skill flow.

Mining and wake-up: **`mempalace-mine-mcp`** exposes **`mempalace_mine`**; the bridge script runs **`mempalace mine`** then **`mempalace wake-up`** with captured stdout and writes **`wakeup.md`**. On Windows, child subprocess env forces UTF-8 I/O (**`PYTHONUTF8`** / **`PYTHONIOENCODING`**) and the parent decodes with UTF-8 so Unicode palace text does not fail pipe encoding before **`wakeup.md`** is refreshed. Extension **`agent-ignore`** excludes **`mine_mcp_server.py`** (and chroma) from agent indexing in consumer workspaces. Operators may **`mempalace_reconnect`** on the primary server after layout updates.

IDE integration depends on merged MCP config plus **explicit enablement/reload** where the adapter requires it (**`guide.md`** IDE checklist; configure skill reinforces this).

## Repo-local authoring

This extension repo also maintains **Spectask** specs under **`spec/`** according to **`spec/main.md`**; **`spawn/navigation.yaml`** at the repo root is **maintainer-maintained** (not emitted from **`extsrc/config.yaml`**), e.g. English-prose conventions and contextual methodology reads.
