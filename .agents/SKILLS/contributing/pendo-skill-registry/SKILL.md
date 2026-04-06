---
name: pendo-skill-registry
description: >-
  Maintain the pendo skill registry whenever a skill is added, updated, renamed, or
  removed inside `.agents/SKILLS/pendo/`. Use this skill any time you create a new pendo
  skill, edit an existing one, or delete one — even if the change feels minor. The
  registry consists of two files that must always stay in sync: `README.md`
  (project-level index) and `.agents/SKILLS/pendo/SKILL.md` (the pendo-domain index read
  by other agents). Trigger on any phrase like "add a pendo skill", "update the pendo
  skill", "I made a new skill", "register this skill", or whenever a file is written
  under `.agents/SKILLS/pendo/`. Never skip this step — stale registries cause other
  agents to miss available skills.
---

# Pendo Skill Registry

Whenever a skill is **added**, **modified**, **renamed**, or **removed** inside
`.agents/SKILLS/pendo/`, you must update **both** registry files before finishing the task.

______________________________________________________________________

## Registry Files

| File                            | Purpose                                                  | Audience                                |
| ------------------------------- | -------------------------------------------------------- | --------------------------------------- |
| `README.md`                     | Project-wide skill index at the repo root                | Humans + all agents                     |
| `.agents/SKILLS/pendo/SKILL.md` | Pendo-domain index; loaded when any pendo skill triggers | Agents working in the pendo skill space |

Both files contain a **Skills Table** (see format below). Keep them identical in content for
the pendo section — one is a full project index, the other is the pendo-scoped quick reference.

______________________________________________________________________

## Pendo skill folder naming

Every **skill** under `.agents/SKILLS/pendo/` lives in its own subdirectory. Those subdirectory
names must start with the prefix **`pendo-`** (for example `pendo-feature-rule-quality`, not
`feature-rule-quality`) so agents can find Pendo skills quickly when browsing or searching by
name.

- Set the YAML **`name`** field in that skill’s `SKILL.md` to the **same** string as the folder
  name (the canonical identifier).
- The domain index file `.agents/SKILLS/pendo/SKILL.md` is **not** a skill folder; do not rename
  it with a prefix.

______________________________________________________________________

## When to Run This Skill

Run immediately after any of the following:

- You create a new folder under `.agents/SKILLS/pendo/pendo-<skill-name>/`
- You edit the `name`, `description`, `metadata.pendo_mcp`, `metadata.pendo_api`, or behavior of an existing pendo skill's `SKILL.md`
- You delete or archive a pendo skill folder
- You rename a pendo skill folder

______________________________________________________________________

## Step-by-Step Workflow

### Step 1 — Read the existing registry

Open both files and find the pendo skills table in each:

```bash
cat README.md
cat .agents/SKILLS/pendo/SKILL.md
```

Locate the table that lists pendo skills. It follows this format (see [Table Format](#table-format) below).

______________________________________________________________________

### Step 2 — Enumerate all current pendo skills

List every skill directory that currently exists:

```bash
ls .agents/SKILLS/pendo/
```

For each subdirectory (skip files, skip `SKILL.md` itself), read its frontmatter (including the `metadata` block):

```bash
head -25 .agents/SKILLS/pendo/pendo-<skill-name>/SKILL.md
```

Extract:

- `name` — the canonical skill identifier from frontmatter
- `description` — the first sentence only (keep it ≤ 20 words for the table cell)
- Folder name — for the link **target** in the Skill column; optional **Pretty Case** label for link **text** (see [Table Format](#table-format))
- `metadata.pendo_mcp` — boolean; table shows **✅** if `true`, **❌** if `false`
- `metadata.pendo_api` — boolean; table shows **✅** if `true`, **❌** if `false`

Every pendo skill **must** declare both booleans under `metadata` so the registry stays accurate.

______________________________________________________________________

### Step 3 — Rebuild the table

Construct a fresh table from the enumerated skills. **Do not rely on the old table** — always
regenerate from the actual folder contents so deletions are automatically reflected.

See [Table Format](#table-format) for the exact schema.

______________________________________________________________________

### Step 4 — Update `README.md`

Replace the existing pendo skills table block in `README.md` with the new table.

The block is delimited by these HTML comments — preserve them exactly:

```markdown
<!-- pendo-skills-start -->
...table here...
<!-- pendo-skills-end -->
```

If the delimiters don't exist yet, add them in the appropriate section of `README.md`
(under a `## Pendo Skills` heading, creating it if needed).

______________________________________________________________________

### Step 5 — Update `.agents/SKILLS/pendo/SKILL.md`

Replace the skills table in `pendo/SKILL.md` with the **same rows** as `README.md`
(**What it does**, **MCP**, **API** must match). For the **Skill** column only, use
**relative** links from `pendo/SKILL.md` to each skill’s `SKILL.md`, e.g.
`[**Feature Rule Quality**](./pendo-feature-rule-quality/SKILL.md)` — not the repo-root
paths used in `README.md`. That way users who copy the whole `pendo/` tree into another
skills folder keep working links.

The block uses the same delimiters:

```markdown
<!-- pendo-skills-start -->
...table here...
<!-- pendo-skills-end -->
```

If the section doesn't exist yet in `pendo/SKILL.md`, add it under a
`## Available Pendo Skills` heading near the top of the file.

______________________________________________________________________

### Step 6 — Verify

Confirm both files have up-to-date tables: same skills and same **What it does** / **MCP** / **API** cells; `pendo/SKILL.md` uses relative **Skill** links as above.

```bash
grep -A 50 "pendo-skills-start" README.md
grep -A 50 "pendo-skills-start" .agents/SKILLS/pendo/SKILL.md
```

If they diverge, fix the discrepancy before finishing.

______________________________________________________________________

## Table Format

In **`README.md`**, link each skill from the repo root:

```markdown
<!-- pendo-skills-start -->
## Pendo Skills

| Skill | What it does | MCP | API |
| --- | --- | :---: | :---: |
| [**Aggregation Builder**](.agents/SKILLS/pendo/pendo-aggregation-builder/) | Use this skill when the user wants to query Pendo data using the Aggregation API. | ❌ | ✅ |
| [**Feature Naming Convention**](.agents/SKILLS/pendo/pendo-feature-naming-convention/) | Audits Pendo feature names against a naming convention template to improve discoverability in analytics dropdowns. | ✅ | ❌ |
| [**Feature Rule Quality**](.agents/SKILLS/pendo/pendo-feature-rule-quality/) | Score feature CSS rules or pasted selectors for stability (0–100); JSON file from `fetch_features.py`, JSON on stdout from `--json`. | ❌ | ✅ |
| [**Page Naming Convention**](.agents/SKILLS/pendo/pendo-page-naming-convention/) | Audits Pendo page names against a naming convention template to improve discoverability in analytics dropdowns. | ✅ | ❌ |
<!-- pendo-skills-end -->
```

In **`.agents/SKILLS/pendo/SKILL.md`**, use the same table content as `README.md` except
the **Skill** column: link with paths **relative to `pendo/SKILL.md`**, targeting each
skill’s `SKILL.md` (recommended: `[**Aggregation Builder**](./pendo-aggregation-builder/SKILL.md)`).
Trailing-slash folder links (e.g. `./pendo-aggregation-builder/`) are acceptable but
prefer `./<folder>/SKILL.md` for a clear open target.

**Rules:**

- Each skill’s folder on disk **must** be named `pendo-<slug>` and match the YAML **`name`**
  field. The **Skill** column link **target** in the domain index must be that folder’s
  `SKILL.md` (or the folder URL) relative to `pendo/SKILL.md`.
- For the **Skill** column **link text** (what readers see), you may **drop** the `pendo-`
  prefix, **replace hyphens with spaces**, and write the rest in **Proper Case** (title case:
  capitalize each word).
  Example: folder `pendo-feature-rule-quality` → visible label **Feature Rule Quality**,
  as in `[**Feature Rule Quality**](./pendo-feature-rule-quality/SKILL.md)` in the domain
  index and `[**Feature Rule Quality**](.agents/SKILLS/pendo/pendo-feature-rule-quality/)` in `README.md`.
  You may use the raw folder name as link text instead if you prefer, but the Pretty Case form
  is recommended for readability in the table.
- **What it does** is the first sentence of the skill's `description` frontmatter, trimmed to ≤ 20 words.
- **MCP** and **API** come from `metadata.pendo_mcp` and `metadata.pendo_api` in that skill's frontmatter: `true` → ✅, `false` → ❌. Center those columns with `| :---: |` in the header separator row.
- Rows are sorted **alphabetically** by skill folder name.
- Never add skills that don't have a corresponding folder on disk.
- Never leave skills in the table whose folder has been deleted.

______________________________________________________________________

## Quality Checklist

Before marking the task complete, confirm:

- [ ] `README.md` table reflects every folder currently in `.agents/SKILLS/pendo/`
- [ ] `.agents/SKILLS/pendo/SKILL.md` table matches `README.md` (**What it does**, **MCP**, **API**); **Skill** links are relative (`./pendo-…/SKILL.md`), not repo-root paths
- [ ] No deleted skill folders appear in either table
- [ ] No undocumented skill folders are missing from either table
- [ ] Rows are alphabetically sorted
- [ ] **MCP** / **API** cells match each skill's `metadata.pendo_mcp` / `metadata.pendo_api`
- [ ] Both delimiter comments (`<!-- pendo-skills-start -->` / `<!-- pendo-skills-end -->`) are present in both files
- [ ] Every skill folder under `.agents/SKILLS/pendo/` is named `pendo-…` and matches its `SKILL.md` `name` field
- [ ] Each Skill column link points at the correct `pendo-…` folder (link text may use Proper Case with the `pendo-` prefix omitted)
