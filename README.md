> [!IMPORTANT]
> This repository is in **beta**: we're still shaping things up, so you may see layout, docs, or skills shift over the next few weeks as we iterate.

---

<img src="docs/professor-pendo.png" align="right" alt="<Image: Professor Pendo logo/brand>" width="250" />

### _Clean data isn't a luxury; it's the signal. Let's fix yours._

#### **Professor Pendo**

---

The **Professor** is an Agent who helps **Pendo** admins run a cleaner subscription: clear naming, stable tagging, and guidance you can act on.

This project ships with many **agent skills** under `.agents/SKILLS/pendo/`: one folder per skill, each with a `SKILL.md`. See [**how to install**](#getting-started) them below.

## Example prompts

Paste or adapt these in chat. With [**Pendo MCP**](https://support.pendo.io/hc/en-us/articles/41102236924955-Connect-to-the-Pendo-MCP-server-beta) connected, your assistant can often pull live data to support answering. **Scope each prompt** (time window, max rows, or “this selector only”) so the assistant doesn’t walk the whole subscription.

- _**Pages** with definitions updated in the last **90 days**. Which names break our naming convention?_
- _**Features** with definitions updated in the last **60 days**. Which names break our naming convention?_
- _For **features** updated in the last **30 days**, pull rules, score each selector, flag the weakest._
- _Score this selector only for tagging stability (0-100). No subscription-wide pull:_ `button:contains('Home')`
- _These two selectors only. Which survives a UI refactor better?_ `.segment-chooser` _vs_ `[data-testid="segment-chooser"]`
- _**Pages** updated in the last **14 days**. Any duplicates (same URL or rule intent)?_
- _Aggregation: count visitors who clicked Feature X in the last **7 days** (not all-time)._

---

## Skills Library

<!-- pendo-skills-start -->
## Pendo Skills

| Skill | What it does | MCP | API |
| --- | --- | :---: | :---: |
| [**Aggregation Builder**](.agents/SKILLS/pendo/pendo-aggregation-builder/) | Understand, build, or verify Pendo Aggregation API pipelines and natural-language analytics queries. | ❌ | ✅ |
| [**Feature Naming Convention**](.agents/SKILLS/pendo/pendo-feature-naming-convention/) | Audit Pendo **feature** names for consistent, readable labels; explains why naming matters. | ✅ | ❌ |
| [**Feature Rule Quality**](.agents/SKILLS/pendo/pendo-feature-rule-quality/) | Score feature CSS rules or pasted selectors for stability (0-100); JSON file from `fetch_features.py`, JSON on stdout from `--json`. | ❌ | ✅ |
| [**Page Naming Convention**](.agents/SKILLS/pendo/pendo-page-naming-convention/) | Audit Pendo **page** names for consistent, readable labels; explains why naming matters. | ✅ | ❌ |
<!-- pendo-skills-end -->

---

## Getting Started

In order to install these skills, you're just moving folders into the right place - no extra setup needed.

1. **Get the repo**: [download the ZIP](https://github.com/boonhapus/professor-pendo/archive/refs/heads/main.zip) and unzip, or clone this repo.
2. **Open** `.agents/SKILLS/pendo/`. Copy **each whole skill folder** (not just `SKILL.md`).
3. **Drop them into** the folder your tool expects:

| Tool | Windows | Mac |
| --- | --- | --- |
| **Cursor** | `.agents\skills\` at the project root | `.agents\skills\` at the project root |
| **Claude Code** | `%USERPROFILE%\.claude\skills\` | `~/.claude/skills/` |
| **Gemini CLI** | `.gemini\skills\` in the workspace | `.gemini/skills/` in the workspace |
| **Claude Desktop** | Custom instructions, project files, or attach `SKILL.md` | Custom instructions, project files, or attach `SKILL.md` |
| **Other chat apps** | Custom instructions, uploads, or paste from this repo | Custom instructions, uploads, or paste from this repo |

Reload or restart if your app requires it.

## Contributing

All contributions are welcome :heart: from bug reports, ideas, to pull requests. Every bit helps!

- **Human contributors:** Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before getting started.
- **AI agents & copilots:** Please read [`.agents/AGENTS.md`](./.agents/AGENTS.md) before making any changes.
