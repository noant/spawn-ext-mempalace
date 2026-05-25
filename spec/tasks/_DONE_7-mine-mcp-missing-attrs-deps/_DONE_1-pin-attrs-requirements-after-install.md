# 1-pin-attrs-requirements-after-install

## Goal
Pin and install **`attrs>=22.2.0`** alongside **`mempalace`** so extension add/update resolves the jsonschema/Chroma dependency chain.

## Approach
1. Update **`extsrc/files/.mempalace/ext/requirements-mempalace.txt`**:
   - Keep **`mempalace==3.3.5`** (sync with **`MEMPALACE_PYPI_VERSION`**).
   - Add **`attrs>=22.2.0`** with a short comment referencing jsonschema/Chroma (not a duplicate of MemPalace pin comment).
2. Update **`extsrc/setup/after_install.py`**:
   - Prefer **`pip install -r <repo>/.mempalace/ext/requirements-mempalace.txt`** (path relative to **`Path.cwd()`** consumer root) so requirements file is the single source of truth.
   - Fallback if requirements file missing: keep **`mempalace=={MEMPALACE_PYPI_VERSION}`** plus **`attrs>=22.2.0`** as explicit specs (defensive).
   - Reuse existing **`_install_mempalace_pip`** / uv fallback; extend naming/logging if the helper becomes “install requirements” (minimal rename or docstring only).
   - Do **not** add **`--force-reinstall`** for mempalace; allow pip to **upgrade** attrs when the pin requires it.

## Affected files
- **`extsrc/files/.mempalace/ext/requirements-mempalace.txt`**
- **`extsrc/setup/after_install.py`**
- **`extsrc/config.yaml`** — bump pack **`version`** patch (e.g. **`0.3.2` → `0.3.3`**) so consumers pick up the install fix on extension update.

## Code examples

**requirements-mempalace.txt (after):**

```text
# Pinned to match extsrc/setup/after_install.py (update both when bumping MemPalace).
# attrs: chromadb → jsonschema 4.x requires attrs>=22.2.0 (mine / Chroma backend).
#   pip install -r .mempalace/ext/requirements-mempalace.txt
mempalace==3.3.5
attrs>=22.2.0
```

**after_install.py — install from requirements (sketch):**

```python
def _requirements_file(root: Path) -> Path:
    return root / ".mempalace" / "ext" / "requirements-mempalace.txt"

def _install_from_requirements(root: Path) -> int:
    req = _requirements_file(root)
    if req.is_file():
        spec = f"-r{req}"  # or ["-r", str(req)] in cmd list
        ...
    spec = f"mempalace=={MEMPALACE_PYPI_VERSION}"
    return _install_mempalace_pip(spec)  # extend to accept list or second attrs spec
```

Call **`_install_from_requirements(root)`** from **`main()`** instead of a bare mempalace-only spec, using **`Path.cwd()`** as consumer root (same as init).

## Acceptance
- Fresh **`pip install -r .mempalace/ext/requirements-mempalace.txt`** upgrades stale attrs and allows **`from mempalace.miner import mine`**.
- **`MEMPALACE_PYPI_VERSION`** and requirements mempalace line stay in sync.
