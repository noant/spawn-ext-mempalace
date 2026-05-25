# 3-diagnose-skill-attrs-troubleshooting

## Goal
Document the **`ModuleNotFoundError: No module named 'attrs'`** (and **`pip check`** attrs/jsonschema warnings) in the extension diagnose skill so agents and users can recover without re-debugging.

## Approach
1. Edit **`extsrc/skills/mempalace-diagnose-palace.md`**, section **Pack / Python** (or new bullet under MCP-adjacent symptoms):
   - Symptom: **`mempalace mine`**, **`mempalace_mine`**, or healthcheck fails with **`attrs`** / **`jsonschema`** import errors; **`import mempalace`** may still work.
   - Cause: stale **`attrs<22`** in the same interpreter (common with old **`pdflatex`** pins).
   - Fix: **`pip install -r .mempalace/ext/requirements-mempalace.txt`** or **`pip install "attrs>=22.2.0"`** in the **Spawn/MCP interpreter**; re-run healthcheck.
   - Note: **`pdflatex`** may require **`attrs<19`** — separate venv if both are needed.
2. Keep prose aligned with existing skill tone (imperative checklist, no new frontmatter fields).

## Affected files
- **`extsrc/skills/mempalace-diagnose-palace.md`**

## Acceptance
- Skill mentions healthcheck now covers Chroma import chain (post step 2).
- No changes to **`config.yaml`** skill registration unless filename changes (not expected).
