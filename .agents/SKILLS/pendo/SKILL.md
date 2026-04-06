---
name: pendo
description: >-
  Domain index for skills under `.agents/SKILLS/pendo/`. Lists every Pendo skill
  with a relative path (from this file) to `SKILL.md` and a one-line summary—copy
  the whole `pendo/` tree into another skills directory and links keep working.
---

## Running scripts

Run Pendo skill Python scripts with **`uv run`** (not `python` directly) so dependencies resolve from the project. On **Windows**, you **must** set **`PYTHONIOENCODING=utf-8`** in the shell **before** `uv run` when output includes Unicode (for example emoji or UTF-8 JSON)—otherwise **`UnicodeEncodeError`** can occur.

______________________________________________________________________

# Pendo skills

<!-- pendo-skills-start -->

## Pendo Skills

| Skill                                                                       | What it does                                                                                                                                   | MCP | API |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :-: |
| [**Aggregation Builder**](./pendo-aggregation-builder/SKILL.md)             | Use when the user needs to understand how Pendo Aggregation API pipelines work, compose pipelines, or verify queries.                          | ❌  | ✅  |
| [**Documentation**](./pendo-docs/SKILL.md)                                  | Answer questions about Pendo features, concepts, SDK usage, API integration, and platform capabilities by fetching live documentation.         | ❌  | ❌  |
| [**Feature Naming Convention**](./pendo-feature-naming-convention/SKILL.md) | Audits Pendo feature names for consistent, readable, understandable labels and explains why that matters for analytics and tagged UI elements. | ✅  | ❌  |
| [**Feature Rule Quality**](./pendo-feature-rule-quality/SKILL.md)           | Evaluates Pendo feature CSS element rules for selector stability; scores selectors 0–100 via fetch_features.py and evaluate_selector.py.       | ❌  | ✅  |
| [**Page Naming Convention**](./pendo-page-naming-convention/SKILL.md)       | Audits Pendo page names for consistent, readable, understandable labels and explains why that matters for analytics and segments.              | ✅  | ❌  |

<!-- pendo-skills-end -->
