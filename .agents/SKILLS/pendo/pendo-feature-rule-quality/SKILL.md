---
name: pendo-feature-rule-quality
description: >
  Evaluates Pendo feature CSS element rules for selector stability (resistance to DOM
  changes): `fetch_features.py` writes a JSON file of feature rules, then score each selector
  0–100. Also scores pasted or ad-hoc selectors (Pendo tagging, Cypress/Playwright locators).
  Trigger when the user asks whether a given feature rule or CSS selector is good, stable,
  strong, or brittle; wants to audit or list tagged features and their rules; compare
  two selectors; or uses casual phrases like "pull my Pendo features", "score my tags",
  or "is this selector OK for Pendo?"
  Machine-readable output: JSON file from `fetch_features.py`; one JSON object on stdout from
  `evaluate_selector.py --json`. Field names and types are under "Machine-readable JSON reference".
metadata:
  version: 0.2.3
  pendo_mcp: false
  pendo_api: true
---

# Feature rule quality (CSS selector stability)

**Primary intent:** help Pendo admins **inspect feature tagging** by combining **live rule data** from Pendo with **objective stability scores** for each CSS selector in `elementPathRules`.

Two scripts work together:

| Script                         | Role                                                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| `scripts/fetch_features.py`    | Writes a **JSON file** of features and their `rules` (CSS selectors). Nothing on stdout. |
| `scripts/evaluate_selector.py` | Scores a single selector **0–100** with bonuses, penalties, and a grade.                 |

Standalone selector questions (no subscription) use **only** `evaluate_selector.py`.

### Terminal encoding (Python)

`evaluate_selector.py` prints **Unicode** to the terminal: emoji in the default (human) report, and the `grade_emoji` field when using `--json`. On **Windows**, Python often uses a legacy console code page, which raises **`UnicodeEncodeError`** when printing those characters.

**Before every `uv run` … `evaluate_selector.py` on Windows**, set UTF-8 for Python—do **not** wait for an error:

| Shell          | Command                                                      |
| -------------- | ------------------------------------------------------------ |
| PowerShell     | `$env:PYTHONUTF8 = "1"` or `$env:PYTHONIOENCODING = "utf-8"` |
| Command Prompt | `set PYTHONUTF8=1` or `set PYTHONIOENCODING=utf-8`           |

On **macOS/Linux**, terminals are usually UTF-8; use the same variables if you still see encoding errors.

`fetch_features.py` writes JSON to a file only; it does not print feature data to stdout. It logs to stderr—if those logs ever fail to encode, use the same variables.

**Machine-readable output:** `fetch_features.py` (**only** output path below) writes **one UTF-8 JSON file**; it does not print JSON to stdout. `evaluate_selector.py --json` prints **one pretty-printed JSON object** per run to **stdout** (indent 2). Default `evaluate_selector.py` output (without `--json`) is human text, not JSON.

### Machine-readable JSON reference (for agents)

Use this section when parsing output programmatically or summarizing scores without re-reading the Python.

**Fetch script path (JSON file on disk):** `.agents/SKILLS/pendo/pendo-feature-rule-quality/scripts/fetch_features.py` — run with `uv run` from the repo root; see [Fetch features](#1-fetch-features).

| Producer                      | Where JSON goes                                                                                                                        | Shape                                                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `fetch_features.py`           | **File only:** `--output` (default `.data/tmp/pendo_features.json`). UTF-8 JSON on disk; progress and errors on **stderr** (not JSON). | Top-level object with a **`results`** array of feature rows (see [Output shape](#output-shape)). |
| `evaluate_selector.py --json` | **Stdout only**, one JSON object per process (indent 2). Not NDJSON unless you invoke the script once per selector yourself.           | Single object; schema below.                                                                     |

**`evaluate_selector.py --json` fields:**

| Field         | Type    | Meaning                                                                                                                                                         |
| ------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `selector`    | string  | Selector evaluated (trimmed).                                                                                                                                   |
| `score`       | integer | 0–100.                                                                                                                                                          |
| `grade`       | string  | Human label (e.g. `Very Stable`).                                                                                                                               |
| `grade_emoji` | string  | One emoji (e.g. 🟢). On Windows, set [terminal encoding](#terminal-encoding-python) **before** `uv run` so JSON stdout does not raise **`UnicodeEncodeError`**. |
| `bonuses`     | array   | Each item is a **two-element array**: `[description, points]`, e.g. `["Data test attribute", 50]`.                                                              |
| `penalties`   | array   | Same structure as `bonuses`.                                                                                                                                    |
| `details`     | object  | Optional booleans/counts from scoring (camelCase keys); omitted keys are not included.                                                                          |

**Minimal example (`evaluate_selector.py --json`):**

```json
{
  "selector": "[data-testid=submit]",
  "score": 100,
  "grade": "Very Stable",
  "grade_emoji": "🟢",
  "bonuses": [["Data test attribute", 50]],
  "penalties": [],
  "details": { "dataTestAttribute": true, "depth": 1 }
}
```

**Using the JSON:** After `fetch_features.py` succeeds, open the **`--output`** file (default `.data/tmp/pendo_features.json`); it is the **only** place feature export JSON is written. Parse it as JSON (e.g. read `results` for the feature list; each item has `rules` as an array of selector strings). For `evaluate_selector.py --json`, parse the process **stdout** as a single JSON object (`score`, `bonuses`, `penalties`, etc.).

Example — machine-readable score for one selector (stdout is JSON). On Windows, set [terminal encoding](#terminal-encoding-python) first:

```bash
uv run .agents/SKILLS/pendo/pendo-feature-rule-quality/scripts/evaluate_selector.py --json "[data-testid=submit]"
```

______________________________________________________________________

## When to use

**Pendo subscription / rules in-app**

- User wants to **audit**, **review**, **export**, or **list** features **with their CSS rules**
- User asks whether rules or selectors are **good**, **stable**, **strong**, **fragile**, or **risky**
- User wants **scores for tagged features** or **recently updated** feature rules
- User asks for Pendo feature metadata **and** selector quality (this skill replaces a separate “fetch only” workflow)

**Ad-hoc selectors (no API)**

- User pastes a selector and asks if it is **good for Pendo**, **stable**, or **strong**
- User compares two selectors or mentions **flaky locators** / **brittle tests**

> **Important:** Pendo MCP `searchEntities` does **not** return `elementPathRules`. Use `fetch_features.py` whenever **rules** are required.

______________________________________________________________________

## Workflow: evaluate rules from Pendo

### 1. Fetch features

From the **repository root** (so `uv` resolves the project and `.env`):

```bash
uv run .agents/SKILLS/pendo/pendo-feature-rule-quality/scripts/fetch_features.py \
  --subscription-id <ID> \
  --integration-key <KEY>
```

The script **writes only a JSON file** (default `.data/tmp/pendo_features.json`); it does not emit JSON on stdout. See [Fetch script reference](#fetch-script-reference) for filters and flags.

**Prerequisites:** `uv`; `PENDO_SUBSCRIPTION_ID` and `PENDO_INTEGRATION_KEY` (flags or `.env`). Optional: `PENDO_DATA_ENVIRONMENT` (`io` | `eu` | `us1` | `jpn` | `au`).

### 2. Score each rule

On **Windows**, set [terminal encoding](#terminal-encoding-python) **before** these commands. For every string in each feature’s `rules` array, run:

```bash
uv run .agents/SKILLS/pendo/pendo-feature-rule-quality/scripts/evaluate_selector.py "<selector>"
# Machine-readable JSON on stdout:
uv run .agents/SKILLS/pendo/pendo-feature-rule-quality/scripts/evaluate_selector.py --json "<selector>"
```

Features with **empty** `rules` are not element-tagged (track events / auto-capture, etc.) — say so instead of scoring.

### 3. Report to the user

- Follow [Presenting results](#presenting-results) (emoji + score for **every** selector evaluated).
- For **≤ 20** features in scope, a table is appropriate: **Display name** (linked), **Product area**, **Author**, **Last updated**, **Rules** with **score + grade per rule** (e.g. `` `selector` → 🟢 92/100 ``).
- For **> 20** features: summary counts, worst/best examples, offer filters — per [Tables and counts](#tables-and-counts).
- **Keep** the JSON output file unless the user asks to remove it.

______________________________________________________________________

## Workflow: pasted or standalone selectors

Use **only** `evaluate_selector.py` (paths as above). On **Windows**, set [terminal encoding](#terminal-encoding-python) before `uv run`. Same scoring model and [presentation rules](#presenting-results).

______________________________________________________________________

## Fetch script reference

PEP 723 `uv` script — dependencies resolve automatically; only **`uv`** is required on the machine.

### CLI

```
uv run path/to/fetch_features.py [OPTIONS]
```

| Flag                 | Env variable             | Default                         | Purpose                                     |
| -------------------- | ------------------------ | ------------------------------- | ------------------------------------------- |
| `--subscription-id`  | `PENDO_SUBSCRIPTION_ID`  | *(required)*                    | Subscription ID                             |
| `--integration-key`  | `PENDO_INTEGRATION_KEY`  | *(required)*                    | Integration key                             |
| `--data-environment` | `PENDO_DATA_ENVIRONMENT` | `io`                            | Region: `io`, `eu`, `us1`, `jpn`, `au`      |
| `--output`           | —                        | `.data/tmp/pendo_features.json` | JSON output path                            |
| `--app-id`           | —                        | `-323232`                       | Filter to one Pendo app                     |
| `--product-area`     | —                        | —                               | Exact Product Area name                     |
| `--author`           | —                        | —                               | Exact `createdByUser.username`              |
| `--updated-since`    | —                        | —                               | `YYYY-MM-DD` — features updated on or after |
| `--created-since`    | —                        | —                               | `YYYY-MM-DD` — features created on or after |

**Behaviour:** JSON is written **only** to the output file. Progress and errors go to **stderr** (structlog, newline-delimited JSON). Exit `0` = success, `1` = HTTP/parse error.

### Output shape

Top-level object with a `results` array. Each feature includes:

| Field           | Description                                      |
| --------------- | ------------------------------------------------ |
| `id`            | Feature id                                       |
| `displayName`   | Feature name in Pendo                            |
| `author`        | Creator username                                 |
| `lastUpdatedAt` | Epoch **milliseconds**                           |
| `rules`         | CSS selectors (`elementPathRules`); may be empty |
| `productArea`   | Product Area name                                |

______________________________________________________________________

## Scoring overview (`evaluate_selector.py`)

**Baseline: 50**, then bonuses and penalties; final score **clamped 0–100**.

### Bonuses

| Rule                    | Points | Signals                                         |
| ----------------------- | -----: | ----------------------------------------------- |
| Data test attribute     |    +50 | `[data-testid=…]`, `[data-cy=…]`, `[data-qa=…]` |
| Semantic data attribute |    +35 | Other `data-*` or custom attrs                  |
| ARIA                    |    +25 | `[aria-label=…]`, `[role=…]`                    |
| Static ID               |    +25 | `#id` / `[id="…"]` (non-generated)              |
| Semantic class          |    +20 | `.btn`, `.modal`, `.card`, …                    |
| Name attribute          |    +15 | `[name="…"]` on forms                           |
| Semantic href           |    +15 | Path-based `href`, not hash/UUID                |

### Penalties

| Rule                    |            Points | Signals                         |
| ----------------------- | ----------------: | ------------------------------- |
| Deep selector           | −8 × extra levels | More than two combinator levels |
| Dynamic class           |       −35 × count | Hashed/CSS-in-JS classes        |
| Positional              |       −30 × count | `:nth-child`, `:first-child`, … |
| Implementation class    |               −25 | Tailwind/Bootstrap utilities    |
| Bare HTML element       |               −25 | Lone `button`, `div`, …         |
| Unqualified generic tag |               −20 | `div` / `span` alone            |
| Text / `:contains`      |       −15 × count | Text-based matching             |
| Adjacent combinator     |               −15 | `+` / `~`                       |

### Grades

| Score  | Grade           |
| ------ | --------------- |
| 85–100 | 🟢 Very Stable  |
| 50–84  | 🔵 Stable       |
| 25–49  | 🟡 Fragile      |
| 0–24   | 🔴 Very Fragile |

______________________________________________________________________

## Presenting results

> **Always include the grade emoji and numeric score** for every evaluated selector — including inline comparisons and quick answers. Do not call a selector “stable” or “fragile” without **e.g. 🟢 92/100**.

For each evaluation:

1. **Score and grade** first
1. **Bonuses** (if any)
1. **Penalties** (if any)
1. **One-sentence recommendation** (e.g. add `data-testid`, avoid `:nth-child`, etc.)

Multiple selectors: evaluate each and recommend the best.

### Feature deep-links

`https://{domain}/s/{subscriptionId}/features/{featureId}`

- `featureId` = `id` from JSON
- `subscriptionId` = same as `--subscription-id`
- `domain` by data environment (same mapping as `professor_pendo.api.PendoAPI`):

| Env   | Domain             |
| ----- | ------------------ |
| `io`  | `app.pendo.io`     |
| `eu`  | `app.eu.pendo.io`  |
| `us1` | `us1.app.pendo.io` |
| `jpn` | `app.jpn.pendo.io` |
| `au`  | `app.au.pendo.io`  |

### Tables and counts

- **≤ 20** features: table with **Display name** (markdown link), **Product area**, **Author**, **Last updated**, **Rules** (selectors + scores). Omit a separate ID column.
- **> 20**: total count; offer filter/search; detailed slices still follow the same row shape when ≤ 20 rows.

______________________________________________________________________

## Common recommendations

- **Score below 50:** suggest `data-testid` / `data-cy`
- **Dynamic classes:** CSS-in-JS churn; prefer data attributes
- **Positional selectors:** anchor to ID or stable attribute
- **Deep chains:** flatten or scope to a stable ancestor
- **Bare tags:** add class or attribute qualifiers

______________________________________________________________________

## Example (`evaluate_selector.py`)

```
Selector : [data-testid="submit-btn"]
Score    : 100/100  🟢 Very Stable

Bonuses:
  ✅  +50  Data test attribute
```

```
Selector : div:nth-child(3) > span.css-a1b2c3
Score    : 0/100  🔴 Very Fragile

Penalties:
  ❌  -35  Dynamic class ×1
  ❌  -30  Positional selector ×1
  ❌  -25  Bare HTML element
  ❌  -20  Unqualified generic tag
```
