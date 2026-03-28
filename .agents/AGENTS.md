# AGENTS.md

Agent-oriented context for **professor-pendo**. This file follows the open [AGENTS.md](https://agents.md/) idea: predictable instructions for coding agents working in this repository.

## Project overview

This repository is primarily a **distribution channel for agent skills** aimed at **Pendo subscription administrators**. The skills under [.agents/PENDO-SKILLS/](PENDO-SKILLS/) encode operational practices—naming, governance, feature rules, selector stability, and related workflows—so teams can **standardize and scale** how they run Pendo.

Each skill lives in its own folder with a `SKILL.md`; some include `scripts/` for repeatable checks or helpers. Browse [PENDO-SKILLS/](PENDO-SKILLS/) for the current set (for example `feature-naming`, `page-naming`, `css-selector-stability`, `get-pendo-feature-rules`).

## Instructions for coding agents

### CSS selector stability (Pendo tagging, tests, locators)

When the user asks about **selector quality or stability**, **whether a selector is a good idea for Pendo** (or Cypress, Playwright, Selenium, etc.), **which of two selectors is better**, **brittle or flaky locators**, or **feedback on a pasted CSS selector** (including `:contains`, `data-testid`, classes, etc.):

1. Read and follow [PENDO-SKILLS/css-selector-stability/SKILL.md](PENDO-SKILLS/css-selector-stability/SKILL.md) end-to-end.
2. From the **repository root**, run the bundled evaluator so dependencies resolve correctly:

   ```bash
   uv run .agents/PENDO-SKILLS/css-selector-stability/scripts/evaluate_selector.py "<selector>"
   uv run .agents/PENDO-SKILLS/css-selector-stability/scripts/evaluate_selector.py --json "<selector>"
   ```

3. Answer using the skill’s format: **score and grade** first, then **bonuses** and **penalties**, then a **one-sentence recommendation**.

On **Windows**, if `uv run` raises `UnicodeEncodeError` when printing (emoji in grades), enable UTF-8 for that shell before running, for example PowerShell: `$env:PYTHONUTF8 = "1"` (or `$env:PYTHONIOENCODING = "utf-8"`). Then human output and `--json` both work.

### Other Pendo skills

For naming, governance, feature rules, and other workflows, open the matching folder under [PENDO-SKILLS/](PENDO-SKILLS/) and follow its `SKILL.md` (and any `scripts/` there).

## Contributing to this repository

For **how to contribute code** to this repo—layout, conventions, and how to work with the Python package when changing behavior—see [CONTRIBUTING-SKILLS/SKILL.md](CONTRIBUTING-SKILLS/SKILL.md).

## Python package: Pendo API client

[src/professor_pendo/api.py](../src/professor_pendo/api.py) holds this project's **Pendo Engage API client**: code that calls Pendo's REST API to support **scripts and automation** alongside the skills. For detailed guidance on extending or using that code, prefer [CONTRIBUTING-SKILLS/SKILL.md](CONTRIBUTING-SKILLS/SKILL.md).

## Setup

Use **[uv](https://github.com/astral-sh/uv)** for installs and day-to-day project commands. From the repository root:

- `uv sync`

If you run Pendo-connected scripts locally, copy [.env.sample](../.env.sample) to `.env` (or otherwise supply the same variables through your environment) and keep secrets out of version control.

## Testing

There is no automated test suite in the tree yet. When tests are added, run whatever the project documents (for example CI or `uv` invocations) and fix failures before finishing a change.

## Security

Do **not** commit Pendo integration keys or other subscription secrets. Treat data retrieved via the API or skills as sensitive to the customer's subscription.
