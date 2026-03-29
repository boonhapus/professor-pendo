---
name: get-pendo-feature-rules
description: >
  Fetches Pendo features via the Aggregation API, returning each feature's id, display
  name, author, last-updated timestamp, CSS element rules, and product area. Use this
  skill whenever the user wants to list, retrieve, search, or export Pendo features —
  including questions like "what features do I have in Pendo?", "show me all my Pendo
  features", "get feature rules from Pendo", or "pull feature metadata from Pendo".
  Always use this skill when Pendo feature data is needed, even if the user phrases it
  casually.
metadata:
  version: "0.1.0"
---

# get-pendo-feature-rules

Retrieves feature metadata and CSS element rules from Pendo using the Aggregation API pipeline. The primary use case is rule inspection and auditing: understanding which CSS selectors Pendo uses to identify each tagged feature.

---

## Bundled script

A ready-to-run Python script lives at `scripts/fetch_features.py` (under this skill folder). It is a **PEP 723** `uv` script — dependencies (including `professor-pendo`, `cyclopts`, `niquests`, `structlog`, and `python-dotenv`) resolve automatically. The only requirement on the machine is **`uv`**.

### Prerequisites

1. **Install `uv`** (if not already present):
   [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

2. **Credentials** — you need two values from Pendo:

   | Value | Where to find it |
   |-------|-----------------|
   | Subscription ID | Settings → Subscription |
   | Integration Key | Settings → Integrations → Integration Keys |

   Optionally place them in a `.env` file in the working directory so you don't need to pass flags every time:

   ```dotenv
   PENDO_SUBSCRIPTION_ID=123456
   PENDO_INTEGRATION_KEY=your-key-here
   PENDO_DATA_ENVIRONMENT=io   # optional; io | eu | us1 | jpn | au
   ```

---

### CLI reference

```
uv run path/to/fetch_features.py [OPTIONS]
```

All flags override their corresponding `.env` / environment variable.

| Flag | Env variable | Type | Default | Purpose |
|------|-------------|------|---------|---------|
| `--subscription-id` | `PENDO_SUBSCRIPTION_ID` | int | *(required)* | Pendo subscription ID |
| `--integration-key` | `PENDO_INTEGRATION_KEY` | str | *(required)* | Pendo integration key |
| `--data-environment` | `PENDO_DATA_ENVIRONMENT` | str | `io` | Region: `io`, `eu`, `us1`, `jpn`, `au` |
| `--output` | — | path | `pendo_features.json` | Path to write JSON output |
| `--app-id` | — | int | `-323232` | Filter results to a specific Pendo app |
| `--product-area` | — | str | *(none)* | Filter by Product Area name (exact match) |
| `--author` | — | str | *(none)* | Filter by `createdByUser.username` (exact match) |
| `--updated-since` | — | date `YYYY-MM-DD` | *(none)* | Return only features updated on or after this date |
| `--created-since` | — | date `YYYY-MM-DD` | *(none)* | Return only features created on or after this date |

### Example invocations

```bash
# Minimal — all features for the default app
uv run fetch_features.py --subscription-id 123456 --integration-key abc123

# Filter to a product area, updated in the last week
uv run fetch_features.py \
  --subscription-id 123456 \
  --integration-key abc123 \
  --updated-since 2026-03-20 \
  --product-area "Onboarding"

# Write output to a custom path
uv run fetch_features.py \
  --subscription-id 123456 \
  --integration-key abc123 \
  --output .data/tmp/features_march.json
```

### Output behaviour

- **JSON data** is written **only** to the output file (default `.data/tmp/pendo_features.json`).
- **Progress, counts, and errors** go to **stderr** via `structlog` as newline-delimited JSON. Do not expect `print` output or a summary table from the script.
- Exit code `0` = success, `1` = HTTP or JSON parse error.
- **Keep the output file:** do not delete the JSON after summarizing or presenting results unless the user explicitly asks. It is the durable export and supports follow-up questions.

---

## Output format

The script writes a JSON object with a single `results` array. Each element represents one Pendo feature and contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique Pendo feature identifier |
| `displayName` | string | Human-readable feature name as shown in Pendo |
| `author` | string | Username of the user who created the feature |
| `lastUpdatedAt` | integer | Last-modified timestamp in **epoch milliseconds** |
| `rules` | array of strings | CSS selectors Pendo uses to identify this feature. Empty array means the feature is captured via track events or auto-capture rather than a manually tagged element. |
| `productArea` | string | Product Area the feature belongs to |

### Sample output

```json
{
  "results": [
    {
      "id": "aB1CdEfGhIjKlMnOpQrStUvWxYz",
      "displayName": "Dashboard | Date range picker",
      "author": "jane.smith@example.com",
      "lastUpdatedAt": 1774038454560,
      "rules": [
        ".date-picker__trigger"
      ],
      "productArea": "Onboarding"
    },
    {
      "id": "zY9XwVuTsRqPoNmLkJiHgFeDcBa",
      "displayName": "Dashboard | Export to CSV",
      "author": "john.doe@example.com",
      "lastUpdatedAt": 1771234567890,
      "rules": [
        "[data-cy=\"export-button\"]"
      ],
      "productArea": "Onboarding"
    },
    {
      "id": "mN3oPqRsTuVwXyZaAbBcDdEeFfG",
      "displayName": "Settings | Save preferences",
      "author": "jane.smith@example.com",
      "lastUpdatedAt": 1769876543210,
      "rules": [],
      "productArea": "Core"
    }
  ]
}
```

---

## Aggregation API pipeline (reference)

The script posts this pipeline to:

```
POST https://app.pendo.io/api/v1/aggregation
Content-Type: application/json
x-pendo-integration-key: <INTEGRATION_KEY>
```

> The host varies by `--data-environment`; the `professor-pendo` client selects the correct base URL automatically.

### Base pipeline (as executed by the script)

```json
{
  "response": { "mimeType": "application/json" },
  "request": {
    "pipeline": [
      { "source": { "features": { "appId": -323232 } } },
      {
        "select": {
          "id": "id",
          "displayName": "name",
          "author": "createdByUser.username",
          "lastUpdatedAt": "lastUpdatedAt",
          "rules": "elementPathRules",
          "productArea": "group.name"
        }
      }
    ]
  }
}
```

### Optional filter stages appended by CLI flags

The script appends these stages to the pipeline when their corresponding flags are provided:

```json
{ "filter": "lastUpdatedAt >= <epoch_ms>" }         // --updated-since
{ "filter": "createdAt >= <epoch_ms>" }             // --created-since
{ "filter": "author == \"jane.smith@example.com\"" } // --author
{ "filter": "productArea == \"Onboarding\"" }       // --product-area
```

---

## Presenting results

### Feature deep-links

When linking a display name to Pendo, use:

`https://{domain}/s/{subscriptionId}/features/{featureId}`

- `{featureId}` — the feature `id` from the JSON (only place it appears in the URL).
- `{subscriptionId}` — same value as `PENDO_SUBSCRIPTION_ID` / `--subscription-id`.
- `{domain}` — app host for the subscription's **data environment** (must match API region). Same mapping as `professor_pendo.api.PendoAPI.domain_data_evironment`:

| `PENDO_DATA_ENVIRONMENT` | `{domain}` |
|---|---|
| `io` (default) | `app.pendo.io` |
| `eu` | `app.eu.pendo.io` |
| `us1` | `us1.app.pendo.io` |
| `jpn` | `app.jpn.pendo.io` |
| `au` | `app.au.pendo.io` |

### Tables and counts

- If there are **≤ 20 features**, display a table with columns: **Display name** | **Product area** | **Author** | **Last updated** | **Rules**. Do **not** include a separate ID column.
  - **Display name:** markdown link `[{displayName}](url)` using **Feature deep-links** above.
  - **Last updated:** parse `lastUpdatedAt` from epoch ms to a human-readable timestamp.
  - **Rules:** show the selector strings from `rules` directly — wrap each in backticks; if there are several, separate them clearly (e.g. one per line with `<br>` if the renderer supports HTML in tables).
- If there are **> 20 features**, show a summary count and offer to filter, search, or export further. When you do show a detailed slice (still **≤ 20** rows), use the same table shape and linking rules as above.
- Always note the total number of features returned.
- **Retain the script's output JSON** at the path passed to `--output` (default `.data/tmp/pendo_features.json`); do not delete it automatically after presenting — see **Output behaviour** above.
- **Important:** the Pendo MCP `searchEntities` tool does **not** return `rules`. Always use this script (or a direct Aggregation API call) when rule/selector data is required.