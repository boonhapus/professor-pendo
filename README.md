<img src="docs/professor-pendo.png" align="right" alt="<Image: Professor Pendo logo/brand>" width="250" />

### _Clean data isn't a luxury; it's the signal. Let's fix yours._

#### **— Professor Pendo**

---

The **Professor** is an Agent who helps **Pendo** admins run a cleaner subscription: clear naming, stable tagging, and guidance you can act on.

This project ships with many **agent skills** under `.agents/PENDO-SKILLS/` — one folder per skill, each with a `SKILL.md`. See [**how to install**](#getting-started) them below.

## Example prompts

Paste or adapt these in chat. With [**Pendo MCP**](https://support.pendo.io/hc/en-us/articles/41102236924955-Connect-to-the-Pendo-MCP-server-beta) connected, your assistant can often pull live data to support answering.

- _Audit my recent Pendo **page** against our naming convention and flag what's inconsistent._
- _Audit my recent Pendo **feature** rules, score their rules, and give an explanation._
- _Is this feature rule a bad idea for Pendo tagging? Score it and explain why:_ `button:contains('Home')`
- _Which of these two selectors is more likely to survive a UI refactor?_ `.segment-chooser` _or_ `[data-testid="segment-chooser"]`
- _Do I have any duplicate Pages?_

---

## Skills Library

| Skill | What it does | Pendo MCP |
| --- | --- | :---: |
| **Feature naming** | Audit **feature** names for analytics and dropdowns. | ✅ |
| **Page naming** | Audit **page** names for paths, funnels, and segments. | ✅ |
| **CSS selector stability** | Score and explain **CSS selector** robustness. | ❌ |
| **Feature rules from Pendo** | Fetch **feature metadata and rules** via the Aggregation API. | ❌ |

---

## Getting Started

In order to install these skills, you're just moving folders into the right place - no extra setup needed.

1. **Get the repo** — [download the ZIP](https://github.com/boonhapus/professor-pendo/archive/refs/heads/main.zip) and unzip, or clone this repo.
2. **Open** `.agents/PENDO-SKILLS/`. Copy **each whole skill folder** (not just `SKILL.md`). On disk those folders are named `feature-naming`, `page-naming`, `css-selector-stability`, and `get-pendo-feature-rules`.
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
