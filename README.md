> [!IMPORTANT]
> This repository is in **beta**: we're still shaping things up, so you may see layout, docs, or skills shift over the next few weeks as we iterate.

---

<img src="docs/professor-pendo.png" align="right" alt="<Image: Professor Pendo logo/brand>" width="250" />

### _Clean data isn't a luxury; it's the signal. Let's fix yours._

#### **Professor Pendo**

---

The **Professor** is an Agent who helps **Pendo** admins run a cleaner subscription: clear naming, stable tagging, and guidance you can act on.

This project ships a **`pendo`** skills bundle under `.agents/SKILLS/pendo/`: a domain index `SKILL.md` plus one folder per topic (each with its own `SKILL.md`). See [**how to install**](#getting-started) it below.

## Example prompts

Paste or adapt these in chat. With [**Pendo MCP**](https://support.pendo.io/hc/en-us/articles/41102236924955-Connect-to-the-Pendo-MCP-server-beta) connected, your assistant can often pull live data to support answering.

- _**Pages** with definitions updated in the last **90 days**. Which names break our naming convention?_
- _**Features** with definitions updated in the last **60 days**. Which names break our naming convention?_
- _For **features** updated in the last **30 days**, pull rules, score each selector, flag the weakest._
- _Score this selector only for tagging stability (0-100). No subscription-wide pull:_ `button:contains('Home')`
- _Which survives a UI refactor better?_ `.segment-chooser` _vs_ `[data-testid="segment-chooser"]`
- _**Pages** updated in the last **14 days**. Any duplicates (same URL or rule intent)?_
- _Aggregation: count visitors who clicked Feature X in the last **7 days** (not all-time)._
- _How does guide activation work in Pendo? Pull the official docs and summarize with links._

---

## Skills Library

<!-- pendo-skills-start -->
## Pendo Skills

| Skill | What it does | MCP | API |
| --- | --- | :---: | :---: |
| [**Aggregation Builder**](.agents/SKILLS/pendo/pendo-aggregation-builder/) | Use when the user needs to understand how Pendo Aggregation API pipelines work, compose pipelines, or verify queries. | ❌ | ✅ |
| [**Documentation**](.agents/SKILLS/pendo/pendo-docs/) | Answer questions about Pendo features, concepts, SDK usage, API integration, and platform capabilities by fetching live documentation. | ❌ | ❌ |
| [**Feature Naming Convention**](.agents/SKILLS/pendo/pendo-feature-naming-convention/) | Audits Pendo feature names for consistent, readable, understandable labels and explains why that matters for analytics and tagged UI elements. | ✅ | ❌ |
| [**Feature Rule Quality**](.agents/SKILLS/pendo/pendo-feature-rule-quality/) | Evaluates Pendo feature CSS element rules for selector stability; scores selectors 0–100 via fetch_features.py and evaluate_selector.py. | ❌ | ✅ |
| [**Page Naming Convention**](.agents/SKILLS/pendo/pendo-page-naming-convention/) | Audits Pendo page names for consistent, readable, understandable labels and explains why that matters for analytics and segments. | ✅ | ❌ |
<!-- pendo-skills-end -->

---

## Getting Started

These **skills** are short guides your AI can follow for Pendo naming, tagging, and analytics. Install them into **Cursor**, **Claude Code**, or **Gemini CLI** by copying one folder into the path your tool expects (below).

### Manual install

1. **[Download the ZIP](https://github.com/boonhapus/professor-pendo/archive/refs/heads/main.zip)** and unzip it, or clone this repo.
2. Open **`.agents`** → **`SKILLS`** and copy the **`pendo`** folder (do not rename it).
3. Paste **`pendo`** into the destination for your tool. Copy the whole folder at once, not the subfolders one by one.

| Tool | Windows | Mac |
| --- | --- | --- |
| **Cursor** | `.agents\skills\pendo\` | `.agents/skills/pendo/` |
| **Claude Code** | `%USERPROFILE%\.claude\skills\pendo\` | `~/.claude/skills/pendo/` |
| **Gemini CLI** | `.gemini\skills\pendo\` | `.gemini/skills/pendo/` |

Restart the app (or reload the window) if the skills do not appear right away.

_**Why isn't Claude Desktop and browser chat apps** in the table above? **API skills** need to run **Python** and send **authenticated HTTP requests** (your Pendo integration key, usually via env vars). Those UIs generally do not run that code or wire credentials the way **Cursor** or a **CLI** does._

> [!NOTE]
> **[`.env.sample`](.env.sample)** lists the **environment variable names** Pendo API scripts in this repo expect: `PENDO_SUBSCRIPTION_ID`, `PENDO_INTEGRATION_KEY`, and optionally `PENDO_DATA_ENVIRONMENT` (data region). It ships **without secrets** so credentials never live in git. To use it, copy the file to **`.env`** in the repo root, fill in your values, and keep **`.env`** local (it is **gitignored**).

---

### Install with [uv](https://github.com/astral-sh/uv)

Install [uv](https://github.com/astral-sh/uv), then run the line below. You do **not** need to clone this repo first; the script is [on GitHub here](https://raw.githubusercontent.com/boonhapus/professor-pendo/main/scripts/install-professor-pendo.py).

```bash
uv run https://raw.githubusercontent.com/boonhapus/professor-pendo/main/scripts/install-professor-pendo.py --help
```

Example output:

```
Usage: install-professor-pendo --which WHICH [OPTIONS]

Copy the Pendo skills bundle into the folder Cursor, Claude Code, or Gemini CLI looks for. Run inside a
clone to use the repo copy of the bundle; otherwise the script downloads from GitHub.

┌─ Commands ───────────────────────────────────────────────────────────────────────────────────────────┐
│ --help     Display this message and exit.                                                            │
│ --version  Display application version.                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─ Parameters ─────────────────────────────────────────────────────────────────────────────────────────┐
│ *  --which      cursor, claude (Claude Code), or gemini (Gemini CLI).                                │
│                 [choices: cursor, claude, gemini]                                                    │
│                 [required]                                                                           │
│    --source     auto: use this repo's bundle if present, else download from GitHub. cloned: only use │
│                 .agents/SKILLS/pendo from this clone (fail if missing). github: always download from │
│                 main on GitHub.                                                                      │
│                 [choices: auto, cloned, github]                                                      │
│                 [default: auto]                                                                      │
│    --directory  Project folder for Cursor / Gemini (where .agents or .gemini should live).           │
│    --replace    Overwrite the destination folder if it already exists.                               │
│                 [default: False]                                                                     │
│    --dry-run    Print what would happen without copying or downloading.                              │
│                 [default: False]                                                                     │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Contributing

All contributions are welcome :heart: from bug reports, ideas, to pull requests. Every bit helps!

- **Human contributors:** Please read [`.github/CONTRIBUTING.md`](./.github/CONTRIBUTING.md) before getting started.
- **AI agents & copilots:** Please read [`.agents/AGENTS.md`](./.agents/AGENTS.md) before making any changes.
