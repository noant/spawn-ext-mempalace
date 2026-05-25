# 2-healthcheck-chromadb-import-chain

## Goal
Make **`spawn extension healthcheck mempalace`** detect the same failure as **`mempalace mine`** before MCP tools run.

## Approach
1. Extend **`extsrc/setup/healthcheck.py`** after successful **`import mempalace`**:
   - Import **`mempalace.backends.chroma`** (or **`from mempalace.miner import mine`**) inside the same try block or a follow-up try.
   - Prefer **`mempalace.backends.chroma`** — matches the user traceback root without pulling all of **`miner`**.
2. On **`ModuleNotFoundError`** / **`ImportError`**, emit message that names the missing module (e.g. **`attrs`**) and points to:
   - **`pip install -r .mempalace/ext/requirements-mempalace.txt`**
   - interpreter path (existing behavior).
3. Keep dual stdout/stderr emit for Spawn visibility.
4. Add **`tests/test_healthcheck.py`** (or extend existing test layout):
   - Mock/import test is optional if env lacks mempalace in CI; at minimum unit-test message helper or skip when mempalace not installed — follow **`tests/conftest.py`** patterns.

## Affected files
- **`extsrc/setup/healthcheck.py`**
- **`tests/test_healthcheck.py`** (new, if CI can import mempalace; otherwise document skip)

## Code examples

```python
def main() -> int:
    try:
        import mempalace  # noqa: F401
        from mempalace.backends import chroma  # noqa: F401
    except ImportError as exc:
        _emit(
            "mempalace healthcheck: import failed (mine/MCP need Chroma deps). "
            f"{exc}. Install pinned deps from .mempalace/ext/requirements-mempalace.txt "
            f"(includes attrs>=22.2.0 for jsonschema). Interpreter:\n  {sys.executable}",
        )
        return 1
    ...
```

## Acceptance
- With stale **`attrs 18.2.0`**, healthcheck exits **1** with actionable text (before user hits mine MCP).
- After requirements install with fixed attrs, healthcheck exits **0**.
