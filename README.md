# Professor Pendo

![Professor Pendo](docs/professor-pendo.png)

**Professor Pendo** helps Pendo admins run a cleaner subscription: clear naming, stable tagging, and guidance you can act on.

This project ships with a bunch of **agent skills** under `.agents/PENDO-SKILLS/` — one folder per skill, each with a `SKILL.md`.

---

## Skills

| Skill | What it does | Pendo MCP |
| --- | --- | --- |
| **Feature naming** | Audit **feature** names for analytics and dropdowns. | ✅ |
| **Page naming** | Audit **page** names for paths, funnels, and segments. | ✅ |
| **CSS selector stability** | Score and explain **CSS selector** robustness. | ❌ |
| **Feature rules from Pendo** | Fetch **feature metadata and rules** via the Aggregation API. | ❌ |

---

## Example prompts

Paste or adapt these in chat. With **Pendo MCP** connected, your assistant can often pull live data for naming questions; otherwise, paste lists or exports.

- "Audit my recent Pendo **page** against our naming convention and flag what's inconsistent."
- "Audit my recent Pendo **feature** rules, score their rules, and give an explanation."
- "Is this feature rule a bad idea for Pendo tagging? Score it and explain why: `button:contains('Home')`"
- "Which of these two selectors is more likely to survive a UI refactor? `.segment-chooser` or `[data-testid="segment-chooser"]`"
- "Do I have any duplicate Pages?"

---

## Install skills

You're just moving folders into the right place—no extra setup from this repo before you start.

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