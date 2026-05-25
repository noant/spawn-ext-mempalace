# Step 2: Bump pack version and verify

## Goal
Publish a new extension **`version`** for the pin change and confirm the pack still passes strict layout checks.

## Approach
1. Bump **`extsrc/config.yaml`** **`version`** from **`0.3.1`** to **`0.3.2`** (patch per **`spawn-ext-increment-version`** — dependency pin is consumer-visible).
2. From repo root, run **`spawn extension check . --strict`**.
3. If **`spawn`** CLI is available and a disposable target is practical, run **`spawn extension healthcheck mempalace`** after install in that target (optional smoke; not required to block if CLI missing).

## Affected files
- `extsrc/config.yaml`

## Code examples
```yaml
# extsrc/config.yaml (top-level only)
version: "0.3.2"
```

```bash
spawn extension check . --strict
```
