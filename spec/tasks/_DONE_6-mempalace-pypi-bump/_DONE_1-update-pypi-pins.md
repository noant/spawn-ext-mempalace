# Step 1: Update PyPI pins

## Goal
Set the supported upstream **`mempalace`** release to **3.3.5** in both pin locations.

## Approach
1. Set **`MEMPALACE_PYPI_VERSION = "3.3.5"`** in **`extsrc/setup/after_install.py`** (keep existing comment pointing at PyPI).
2. Set **`mempalace==3.3.5`** in **`extsrc/files/.mempalace/ext/requirements-mempalace.txt`** (keep header comment about parity with the hook).

## Affected files
- `extsrc/setup/after_install.py`
- `extsrc/files/.mempalace/ext/requirements-mempalace.txt`

## Code examples
```python
# extsrc/setup/after_install.py
MEMPALACE_PYPI_VERSION = "3.3.5"
```

```text
# extsrc/files/.mempalace/ext/requirements-mempalace.txt
mempalace==3.3.5
```
