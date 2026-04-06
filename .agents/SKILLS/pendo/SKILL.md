---
name: pendo
description: >
  Domain index for skills under `.agents/SKILLS/pendo/`. Lists every Pendo skill
  with a relative path (from this file) to `SKILL.md` and a one-line summary—copy
  the whole `pendo/` tree into another skills directory and links keep working.
---

## Python scripts and terminal encoding

Skills that run **`uv run`** on Python helpers which **print Unicode** to the terminal (emoji and UTF-8 JSON) currently include [**Feature Rule Quality**](./pendo-feature-rule-quality/SKILL.md) (`scripts/evaluate_selector.py`). On **Windows**, set **`PYTHONUTF8=1`** or **`PYTHONIOENCODING=utf-8`** in the shell **before** `uv run` every time—otherwise Python can raise **`UnicodeEncodeError`**. See [Feature Rule Quality → Terminal encoding (Python)](./pendo-feature-rule-quality/SKILL.md#terminal-encoding-python) for shell commands.

---

# Pendo skills

<!-- pendo-skills-start -->
## Pendo Skills

| Skill | What it does | MCP | API |
| --- | --- | :---: | :---: |
| [**Aggregation Builder**](./pendo-aggregation-builder/SKILL.md) | Use when the user needs to understand how Pendo Aggregation API pipelines work, compose pipelines, or verify queries. | ❌ | ✅ |
| [**Documentation**](./pendo-docs/SKILL.md) | Answer questions about Pendo features, concepts, SDK usage, API integration, and platform capabilities by fetching live documentation. | ❌ | ❌ |
| [**Feature Naming Convention**](./pendo-feature-naming-convention/SKILL.md) | Audits Pendo feature names for consistent, readable, understandable labels and explains why that matters for analytics and tagged UI elements. | ✅ | ❌ |
| [**Feature Rule Quality**](./pendo-feature-rule-quality/SKILL.md) | Evaluates Pendo feature CSS element rules for selector stability; scores selectors 0–100 via fetch_features.py and evaluate_selector.py. | ❌ | ✅ |
| [**Page Naming Convention**](./pendo-page-naming-convention/SKILL.md) | Audits Pendo page names for consistent, readable, understandable labels and explains why that matters for analytics and segments. | ✅ | ❌ |
<!-- pendo-skills-end -->
