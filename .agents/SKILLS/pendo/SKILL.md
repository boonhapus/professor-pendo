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
| [**Aggregation Builder**](./pendo-aggregation-builder/SKILL.md) | Understand, build, or verify Pendo Aggregation API pipelines and natural-language analytics queries. | ❌ | ✅ |
| [**Feature Naming Convention**](./pendo-feature-naming-convention/SKILL.md) | Audit Pendo **feature** names for consistent, readable labels; explains why naming matters. | ✅ | ❌ |
| [**Feature Rule Quality**](./pendo-feature-rule-quality/SKILL.md) | Score feature CSS rules or pasted selectors for stability (0–100); JSON file from `fetch_features.py`, JSON on stdout from `--json`. | ❌ | ✅ |
| [**Page Naming Convention**](./pendo-page-naming-convention/SKILL.md) | Audit Pendo **page** names for consistent, readable labels; explains why naming matters. | ✅ | ❌ |
<!-- pendo-skills-end -->
