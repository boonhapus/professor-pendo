---
name: contributing
description: >-
  Repo-specific conventions after AGENTS.md: set up via CONTRIBUTING.md first, then use
  this skill for layout (skills vs package), pendo-skill-registry when editing Pendo
  skills, and pendo-docs for product questions. Read when changing Python, Markdown,
  tooling, or files under .agents/.
---

# Contributing (agents)

You are changing **this repository**. You have already read [`.agents/AGENTS.md`](../../AGENTS.md) (project shape and `.agents/` layout).

## 1. Environment

Before you finish work that touches Python or Markdown, follow [`.github/CONTRIBUTING.md`](../../../.github/CONTRIBUTING.md) from the repo root:

- `uv sync`
- `uv run prek install` (once per clone)
- When needed: `uv run prek run --all-files`, Ruff, mdformat — as that file describes

Do not duplicate those steps here; CONTRIBUTING.md is the single source of truth for install and quality checks.

## 2. Layout (quick reference)

| What              | Where                    |
| ----------------- | ------------------------ |
| Pendo skills      | `.agents/SKILLS/pendo/`  |
| Python package    | `src/professor_pendo/`   |
| Pendo skills index | [`../pendo/SKILL.md`](../pendo/SKILL.md) |

Pick the folder that matches the task; AGENTS.md is not a full catalog of every skill.

## 3. Nested skill: registry

If you **add, rename, delete, or materially edit** anything under `.agents/SKILLS/pendo/`, follow [**pendo-skill-registry**](pendo-skill-registry/SKILL.md) so `README.md` and `.agents/SKILLS/pendo/SKILL.md` stay in sync.

## 4. Pendo product questions

For “how does X work in Pendo?” (not subscription data), use [**pendo-docs**](../pendo/pendo-docs/SKILL.md) instead of guessing.

## 5. Tests

There is no documented test suite in-tree yet. When CI or the README adds one, run what they specify before finishing a change.

## 6. Security

Do not put integration keys or customer data in commits, skills, or pasted logs.
