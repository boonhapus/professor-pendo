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

**What this does:** Your AI assistant (Cursor, Claude, Gemini, or similar) can follow **skills**: short guides that help it answer Pendo questions the way Professor Pendo intends. Installing means copying one folder from this project into the place your app looks for those guides. There is no installer and no login here; you are just adding files your tool already knows how to read.

1. **[Download the ZIP](https://github.com/boonhapus/professor-pendo/archive/refs/heads/main.zip)** and unzip it (or clone the repo if you use Git).
2. In the project folder, go to **`.agents`** → **`SKILLS`**. Copy the **`pendo`** folder you see there (do not rename it).
3. **Paste `pendo`** into the folder your app uses for skills (see the table below). Copy the folder as one piece, not the smaller folders inside it one by one.

| If you use… | Put the **`pendo`** folder here (Windows) | Put the **`pendo`** folder here (Mac) |
| --- | --- | --- |
| **Cursor** | `.agents\skills\pendo\` next to your project (create `skills` if it is missing) | `.agents/skills/pendo/` next to your project |
| **Claude Code** | `%USERPROFILE%\.claude\skills\pendo\` | `~/.claude/skills/pendo/` |
| **Gemini CLI** | `.gemini\skills\pendo\` in your project folder | `.gemini/skills/pendo/` in your project folder |
| **Claude Desktop** | Often: add a file or folder via **Settings**, or paste content into **Custom instructions**. Use any `SKILL.md` from the `pendo` folder if your app asks for a file. | Same as Windows |
| **Another chat app** | Use that app’s option for custom instructions, uploads, or project files, or paste text from a `SKILL.md` in this repo. | Same as Windows |

Restart the app (or reload the window) if you do not see the new behavior right away.

## Contributing

All contributions are welcome :heart: from bug reports, ideas, to pull requests. Every bit helps!

- **Human contributors:** Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before getting started.
- **AI agents & copilots:** Please read [`.agents/AGENTS.md`](./.agents/AGENTS.md) before making any changes.
