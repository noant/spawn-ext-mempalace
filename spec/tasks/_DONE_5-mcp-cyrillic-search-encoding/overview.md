# 5: MCP search with Cyrillic (UTF-8) on Windows

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
Ensure MemPalace MCP tool calls that carry Cyrillic text (e.g. Russian queries) work reliably when the extension-launched stdio servers run under Windows legacy console encoding.

## Design overview
- Affected modules: **`extsrc/mcp/windows.json`**, **`linux.json`**, **`macos.json`** (**`env`** on both servers everywhere; **`transport.args`** on Windows only for UTF-8 mode); **`extsrc/files/.mempalace/guides/guide.md`**. **`spec/design/hla.md`** was left unchanged at close (maintainer choice).
- Data flow changes: merged **`PYTHONIOENCODING=utf-8`** for every platform; on Windows, UTF-8 **mode** is enabled via **`-X utf8`** in the **`py -3`** argv list (not via **`PYTHONUTF8`** in **`env`** — see **Details**). JSON-RPC **`tools/call`** arguments and **`content`** round-trip Unicode instead of failing or mangling under legacy console defaults.
- Integration points: Spawn MCP merge → IDE stdio adapter → **`python3`** (Unix) or **`py -3 -X utf8`** (Windows pack defaults) → **`mempalace.mcp_server`** (upstream) or **`mine_mcp_server.py`** (pack).

## Before → After
### Before
- Pack **`env`** for MCP servers only sets **`MEMPALACE_PALACE_PATH`**. **`mine_mcp_server.py`** already forces UTF-8 for **child** `mempalace` subprocesses on Windows (**`PYTHONUTF8`** / **`PYTHONIOENCODING`**) but not for the MCP server’s **own** stdin/stdout decoding of JSON lines.
- On Windows, Python may default stdio to a legacy code page; Cyrillic in MCP requests/responses can trigger **`UnicodeEncodeError`** / **`UnicodeDecodeError`** or visible mojibake when the host speaks UTF-8 on the wire.
### After
- **`linux.json`** / **`macos.json`**: both servers gain **`PYTHONIOENCODING=utf-8`** in **`env`** (unchanged **`transport`**).
- **`windows.json`**: both servers gain **`PYTHONIOENCODING=utf-8`** in **`env`**; **`args`** are **`["-3", "-X", "utf8", …]`** so CPython UTF-8 mode is on **without** **`PYTHONUTF8`** in the merged environment.
- **`guide.md`** documents **`PYTHONIOENCODING`**, Windows **`-X utf8`**, why **`PYTHONUTF8`** is avoided in pack **`env`**, and that persistent issues may still be upstream **`mempalace`** / embeddings.

## Details
### Scope assumptions *(blocking ambiguities defaulted — correct in Step 3 if wrong)*
- **Symptom focus:** semantic **search** (and any MCP tool path that echoes Cyrillic) via **`mempalace-mcp`**, not CLI-only **`mempalace search`** unless the user later expands scope.
- **Primary hypothesis:** Windows Python stdio / UTF-8 mode for the **MCP server process**, fixable by pack MCP metadata without forking upstream **`mempalace.mcp_server`**.
- **Out of pack (unless reproduction proves otherwise):** embedding model quality for Russian, Chroma/storage corruption, or IDE bugs unrelated to Python stdio — note as follow-up if the pack changes do not resolve.

### Why not `PYTHONUTF8` in merged `env` (post-ship correction)
CPython accepts **`PYTHONUTF8`** only when it is exactly **`1`** or **`0`**. Some MCP hosts merge or synthesize env such that **`PYTHONUTF8`** is present but **invalid** (e.g. empty), which aborts startup with **`Fatal Python error: preconfig_init_utf8_mode: invalid PYTHONUTF8 environment variable value`**. The pack therefore enables UTF-8 mode with **`-X utf8`** in **`windows.json`** **`transport.args`** instead.

### Constraints
- Keep **`servers[].name`** sets identical across **`windows.json`**, **`linux.json`**, **`macos.json`**; **`transport`** (including **`args`**) and **`env`** may differ per OS where needed.
- Do not commit secrets; new **`env`** values are plain literals (not **`secret`**).
- **`spawn extension check`** (especially **`--strict`**) must stay green.
- Release: bump **`extsrc/config.yaml`** patch **`version`** when publishing (per **`spawn-ext-increment-version`**).

### Verification (implementation phase)
- On Windows: with merged MCP config, MCP connects (**no** fatal **`PYTHONUTF8`** pre-init); invoke a MemPalace search tool with a Cyrillic query (e.g. «проверка») — expect success **or** a normal application-level “no results”, not encoding exceptions in MCP logs.
- Regression: ASCII-only queries still work; **`mempalace_mine`** bridge still completes and writes **`wakeup.md`** when stderr/stdout contain Unicode.

## Execution Scheme
> Original plan: **`_DONE_1-pack-mcp-env-utf8.md`** → **`_DONE_2-docs-and-verify.md`**. Substance retained below; **`PYTHONUTF8`**-in-**`env`** wording from the first draft was superseded by **`-X utf8`** on Windows (see **Details**).

- Phase 1 (sequential): step **`_DONE_1-pack-mcp-env-utf8.md`** → step **`_DONE_2-docs-and-verify.md`**
