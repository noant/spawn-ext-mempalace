# MemPalace (Spawn extension)

[MemPalace](https://pypi.org/project/mempalace/) is local-first memory for assistants: verbatim storage and semantic search (method of loci: wings → rooms → halls → drawers). This **Spawn extension** helps you **install** MemPalace and **create a repo-scoped palace**, **wires MCP into the IDE automatically** (official MemPalace tools plus a mine bridge), and adds **hints**, **skills**, and **wake-up** context the agent is steered to read. Together that keeps palace state fresh on disk, reminds the agent **when to run mine** on the project after substantive edits, and **when to reconnect** the main MCP session so tools see the latest palace—without you re-describing the setup every time.

Official product docs: [getting started](https://mempalaceofficial.com/guide/getting-started), [configuration](https://mempalaceofficial.com/guide/configuration.html).

## Install

### 1. Install Spawn CLI (uv tool)

Install [uv](https://docs.astral.sh/uv/), then install the Spawn command from PyPI into uv’s tools directory (**`spawn` must be on `PATH`** after install — see uv’s docs for tool paths):

```bash
uv tool install spawn-cli
```

Upstream source repository: **github.com/noant/spawn-cli**.

### 2. Initialize the repo and add MemPalace

From the **root of the target git repository**, initialize Spawn once per repo, then install this extension:

```bash
spawn init
spawn extension add https://github.com/noant/spawn-ext-mempalace.git
```

Use your fork or clone URL if you are not installing from that remote.

One line (same result without a prior global install; run from that repo root):

```bash
uvx --from spawn-cli spawn init && uvx --from spawn-cli spawn extension add https://github.com/noant/spawn-ext-mempalace.git
```

After install, Spawn renders pack skills into your IDE. Invoke **`mempalace-configure-palace`** so the agent can help shape the palace for this repo (wings, rooms, `mempalace.yaml`, global `palace_path`, identity), using the merged guides and configuration reference. Use **`mempalace-search`** when you want retrieval steered through MemPalace before plain workspace search.

### Update or remove

From the **root of the target git repository**:

```bash
spawn extension update mempalace
spawn extension remove mempalace
```

Extension ids match the `name` field in this pack’s `extsrc/config.yaml` (`mempalace` for this repository).

## How it works

1. **Install hook:** this pack declares **`setup.after-install`** in `extsrc/config.yaml`, so Spawn **runs** **`setup/after_install.py`** from the installed extension copy right after it **materializes** the pack (e.g. **`spawn extension add`** or **`spawn extension update mempalace`**). That script installs a pinned **`mempalace`** release via pip or **`uv pip`** when pip is missing (unless **`MEMPALACE_EXTENSION_SKIP_PIP`** is set), sets **`MEMPALACE_PALACE_PATH`** to **`<repo>/.mempalace/palace`** for the **`mempalace init`** subprocess when neither that nor **`MEMPAL_PALACE_PATH`** is already inherited (unless **`MEMPALACE_EXTENSION_GLOBAL_PALACE`** opts out), and runs **`mempalace init .`** in the target repo root (unless **`MEMPALACE_EXTENSION_SKIP_INIT`** is set), with **inherited stdin/stdout/stderr** so MemPalace’s prompts stay interactive during the hook. Set **`MEMPALACE_EXTENSION_AUTO_MINE=1`** if you prefer **`--auto-mine`** (longer install, skips the usual mine confirmation). Verify with **`spawn extension healthcheck mempalace`** when the pack declares a healthcheck.
2. **Palace data** defaults to **`MEMPALACE_PALACE_PATH=.mempalace/palace`** (relative to the workspace) via merged MCP **`env`**; the mine bridge aligns when that env is absent. Override with **`--palace`** or a pre-set **`MEMPALACE_PALACE_PATH`**; set **`MEMPALACE_EXTENSION_GLOBAL_PALACE`** to keep MemPalace’s usual **`~/.mempalace/palace`** without editing **`mempalace.yaml`**. For plain shells (**`mempalace search`** outside the IDE), export the same **`MEMPALACE_PALACE_PATH`** or pass **`--palace`** so CLI matches IDE.

3. **MCP**: this pack declares two stdio servers in **`extsrc/mcp/`** (`windows.json`, `linux.json`, `macos.json` — Spawn merges the file for the host OS). **`mempalace-mcp`** runs **`python -m mempalace.mcp_server`** (**`py -3 -X utf8 …`** on Windows, **`python3 -X utf8 …`** on Linux/macOS — see **`extsrc/mcp/*.json`**); **`python -m mempalace mcp`** is upstream setup text only and does **not** host the MCP protocol. **`mempalace-mine-mcp`** runs the bridge script with the same interpreter family. After **`spawn extension add`**, that config merges via Spawn. **`mempalace-mcp`** exposes the official MemPalace tools; **`mempalace-mine-mcp`** exposes **`mempalace_mine`**, which runs **`mempalace mine`** and, on success, **`mempalace wake-up`**, refreshing **`.mempalace/wakeup.md`**. If the main MemPalace MCP server was already connected, call **`mempalace_reconnect`** on **`mempalace-mcp`** so it picks up on-disk updates.
4. **Agents** read **`.mempalace/wakeup.md`** via merged **`spawn/navigation.yaml`** (global required read when populated) and the guides via pack-local required reads. Optional **`hints.global`** in `extsrc/config.yaml` reminds agents to mine and reconnect after substantive edits.

## The `.mempalace/` layout

| Path | Role |
|------|------|
| **`.mempalace/guides/guide.md`** | Install, init, MCP mine/wake-up workflow, links to official docs. |
| **`.mempalace/guides/configuration.md`** | `config.json`, `mempalace.yaml`, env vars, **`MEMPALACE_PALACE_PATH`**, repo-local **`.mempalace/palace`**. |
| **`.mempalace/wakeup.md`** | Bounded wake-up context from the palace; artifact stub until mine or **`mempalace wake-up`** refreshes it. |
| **`.mempalace/ext/`** | `requirements-mempalace.txt` (minimal pip line) and `mine_mcp_server.py` (MCP bridge for **`mempalace_mine`**). |

Palace indices and metadata after **`mempalace init`** live under **`.mempalace/`** — Chroma-backed data defaults to **`.mempalace/palace`** together with MCP and the install hook unless you opted into a global palace. Exact auxiliary tree depends on your installed CLI version.

## Core principles

**One palace per project workflow.** Initialize at the repo root and keep `palace_path` consistent across CLI and MCP so the assistant searches and stores in the same place.

**Mine + wake-up for fresh context.** Mining updates the palace and regenerates **`.mempalace/wakeup.md`**, which is merged into agent navigation as mandatory context. **Merged hints** from this pack **instruct agents** that after tasks involving edits to this repo’s code or documentation they are to call **`mempalace_mine`** (**`mempalace-mine-mcp`**) and then **`mempalace_reconnect`** on **`mempalace-mcp`** when that server was already connected.

**MCP requires a Python env with `mempalace`.** Both servers must run with an interpreter that can execute the **`mempalace`** CLI or module (venv path, `py` on Windows, etc.) — see the shipped **MCP** section in **`.mempalace/guides/guide.md`**.

## Skills

After install, invoke these **skills** by name; Spawn renders them into your IDE’s skill/rules layout.

| Skill | Purpose |
|-------|---------|
| **mempalace-configure-palace** | Configure MemPalace palace settings (global config, project YAML, `palace_path`, identity). |
| **mempalace-search** | Prefer MemPalace MCP or CLI search for semantic recall; fall back to workspace search if needed. |
| **mempalace-diagnose-palace** | Diagnose install, palace path alignment, CLI/MCP, and wake-up context in the target repo. |

## Navigation and reads

**`spawn/navigation.yaml`** (generated by Spawn after install) is the merged index of what agents should read first (`read-required` / contextual reads).

- **`.mempalace/wakeup.md`** is declared with **`globalRead: required`** in this pack so every agent session can load bounded palace context once it exists.
- **`.mempalace/guides/*.md`** use **`localRead: required`** — they appear in this extension’s merged reads for the target pack, not as global entries for unrelated extensions.

Full MCP wiring checklist and skip-env flags are documented in **`.mempalace/guides/guide.md`** after install.

## About

Spawn extension: MemPalace — local-first assistant memory, MCP wiring (official server + mine bridge), repo-scoped palace init, search/configuration/diagnostic skills.

## License

[MIT](LICENSE).
