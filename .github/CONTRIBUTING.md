# Feedback and Contribution

We welcome any input, feedback, bug reports, and contributions via [**Professor Pendo's** GitHub Repository](https://github.com/boonhapus/professor-pendo). :heart:

This page is all you need to **set up your machine**, **run the same checks we use before commits**, and **know where things go** in this repo.

## What you need

- **[Git](https://git-scm.com/)** — clone the repo and version your changes.
- **[uv](https://github.com/astral-sh/uv)** — installs Python and project tools in one reproducible step.

> [!NOTE]
> If you run scripts that call Pendo’s API, copy [`.env.sample`](../.env.sample) to `.env` and fill in values.

## First-time setup (from the repo root)

```bash
uv sync
uv run prek install
```

`uv sync` installs everything this project uses (including **Ruff** for Python, **mdformat** for Markdown, and **prek** for git hooks).  
`prek install` wires up hooks so your commits get checked automatically—run it **once per clone**.

Hook definitions live in [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) (standard filename; we only run hooks through **prek**, not other runners).

## Checks you can run yourself

**Everything the hooks run** (good before you open a PR or after a big pull):

```bash
uv run prek run --all-files
```

**Python** (lint + format):

```bash
uv run ruff check .
uv run ruff format .
```

**Markdown**:

```bash
uv run mdformat .
```

Ruff and mdformat settings are in [`pyproject.toml`](../pyproject.toml).

If a hook fails, fix the issue, then commit again.

## Where to put changes

- **Pendo guidance (skills)** → `.agents/SKILLS/pendo/` — see [`.agents/AGENTS.md`](../.agents/AGENTS.md) for the big picture.
- **Python library** → `src/professor_pendo/`.

If you edit anything under `.agents/SKILLS/pendo/`, keep the Pendo skill registry up to date — see [pendo-skill-registry](../.agents/SKILLS/contributing/pendo-skill-registry/SKILL.md).

## Issues and pull requests

Open an issue when something is broken or you have an idea—include enough detail to reproduce or discuss it.  
Pull requests work best when they’re **small and focused** and **match existing layout and naming**.

## Security

Do not commit API keys or other secrets. Treat anything from a Pendo subscription as sensitive.
