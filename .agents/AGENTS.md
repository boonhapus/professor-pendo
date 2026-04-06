# AGENTS.md

Agent-oriented context for **professor-pendo**. This file follows the open [AGENTS.md](https://agents.md/) idea: predictable instructions for coding agents working in this repository.

**Human-first workflow** (install, Ruff, prek, Markdown, hooks) lives in [`.github/CONTRIBUTING.md`](../.github/CONTRIBUTING.md). Follow that for setup and quality checks; this file does not repeat those steps.

## Project overview

This repository is mainly a **distribution channel for agent skills** aimed at **Pendo subscription administrators**, plus a small **Python package** for Pendo API access used by some scripts.

## What lives under `.agents/`

| Path                                           | Purpose                                                                                                                                                                                                           |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`SKILLS/pendo/`](SKILLS/pendo/)               | **Pendo-domain skills**—operational guidance (naming, analytics, tagging, product documentation, and related workflows). Each topic is its own folder with a `SKILL.md`; some include `scripts/` or `resources/`. |
| [`SKILLS/contributing/`](SKILLS/contributing/) | **Working on this repo**—conventions for agents (layout, nested skills, when to use the registry). Start with [`SKILL.md`](SKILLS/contributing/SKILL.md).                                                         |

Do not treat this file as a catalog of individual skills; open the folder that matches the task and follow its `SKILL.md`.

## Instructions for coding agents

When work matches a skill’s scope, read that skill’s `SKILL.md` (and any `scripts/` or `resources/` it references) and follow it. Run commands from the **repository root** unless the skill says otherwise.

## Python package

[`src/professor_pendo/api.py`](../src/professor_pendo/api.py) is the **Pendo Engage API client** for scripts and automation. For extending it or contributing alongside skills, use [`.github/CONTRIBUTING.md`](../.github/CONTRIBUTING.md) and [`SKILLS/contributing/SKILL.md`](SKILLS/contributing/SKILL.md) as needed.

## Setup

Use **[uv](https://github.com/astral-sh/uv)**. From the repository root: `uv sync`. Full details: [`.github/CONTRIBUTING.md`](../.github/CONTRIBUTING.md).

If you run Pendo-connected scripts locally, copy [`.env.sample`](../.env.sample) to `.env` (or set the same variables another way) and keep secrets out of version control.

## Testing

There is no automated test suite in the tree yet. When tests exist, run what the project documents and fix failures before finishing a change.

## Security

Do **not** commit Pendo integration keys or other subscription secrets. Treat API and skill output as sensitive to the customer’s subscription.
