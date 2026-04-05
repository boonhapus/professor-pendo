---
name: pendo-page-naming-convention
description: >
  Audits Pendo **page** names for consistent, readable, understandable labels and explains
  why that matters for analytics and segments. Trigger when the user asks about page
  naming conventions, consistency, readability, discoverability, or wants an audit of
  Pendo pages (e.g. "check my page names", "which pages break our convention", "badly
  named pages", "recently updated pages"). For **feature** names only, use
  `pendo-feature-naming-convention` instead.
metadata:
  version: "0.1.0"
  pendo_mcp: true
  pendo_api: false
---

# page-naming

Audits Pendo page names against a naming convention and explains why consistent naming matters.

**When to use:** Questions about **Page** entity names—conventions, consistency, readability, discoverability, or audits of recently updated pages. For **Feature** names, use `pendo-feature-naming-convention`.

---

## Why naming conventions matter

Consistent page naming is one of the highest-leverage things a Pendo admin can do. Pages appear as raw names in:
- **Analytics dropdowns** — Paths, Funnels, Retention, and Page analytics reports
- **Dashboard widgets** — where names are the only label shown
- **Segment builder** — used by non-technical stakeholders to build audience rules

A good naming convention makes pages instantly scannable. A bad one — `/?id=324` auto-tagged or `Homepage v2 FINAL` — forces users to mentally decode what screen is being described, and they often just pick the wrong one.

**Keep names short:** The Pendo UI truncates page names at approximately **40 characters** in most dropdowns and name fields. The most specific segment — the View — is the part most likely to be cut off. Aim to stay under 40 characters.

---

## Naming convention

Pages describe *where* a user is — a location, not an action. The structure reads naturally as: *"the [View] is in the [Section] of [Area]."*

> **`[Area] [sep] [Section] [sep] [View]`**
>
> Examples using `>` as separator:
> - `Analytics > Funnels > Report`
> - `Settings > Billing > Payment Methods`
> - `Onboarding > Setup > Company Profile`
> - `Users > Team Management > Invite Members`

**Key distinction from features:** The last segment (View) is a **noun phrase** — the name of the screen or view. It should **not** start with a verb. If you find yourself writing `Settings > Billing > Edit Card`, that's a feature, not a page.

### Separator

The user chooses their own separator. Ask at the start of an audit if none has been established. Use the same separator as the feature naming convention if one is already in use across the account.

| Separator | Example | Notes |
|---|---|---|
| `>` | `Analytics > Funnels > Report` | Clear, readable, widely used |
| `-` | `Analytics - Funnels - Report` | Clean, minimal |
| `\|` | `Analytics \| Funnels \| Report` | High contrast in dropdowns |

**Not recommended:**
- `_` (underscore) — hard to read, looks like a URL slug
- space only — ambiguous, no clear segment boundaries
- raw URL paths (e.g. `/app/settings/billing`) — unreadable in dropdowns

The separator must be used **consistently** across all segments in a name. Mixed separators within a single name are a ⚠️ Minor issue.

### Segment rules

0. **Segment 0 (App Name) — optional** — Some teams prefix all page names with the app name (e.g. `MyApp > Analytics > Funnels > Report`). This is acceptable as long as it is used **consistently across all pages in that app**. If the app name is longer than ~8 characters, flag a ⚠️ warning that it will consume a significant portion of the 40-character limit.
1. **Segment 1 (Area)** — Title Case, 1–3 words. The top-level section of the product (e.g. `Analytics`, `Settings`, `Onboarding`, `Users`).
2. **Segment 2 (Section)** — Title Case, 1–4 words. A subsection or module within the Area (e.g. `Funnels`, `Billing`, `Team Management`).
3. **Segment 3+ (View)** — Title Case noun phrase, 1–4 words. The name of the specific screen or view. Should end with or be a recognized view type word where possible (see reference list below). Must **not** start with a verb. Additional segments beyond 3 are allowed if needed for specificity, but the **total name length must stay under 40 characters**.
4. Each segment must be non-empty after trimming.
5. No double spaces, no leading/trailing spaces per segment.

When evaluating consistency of the app name prefix: if some pages in the same app include the app name segment and others don't, flag the inconsistent ones as ⚠️ Minor.

### Length rule

- ✅ Under 40 characters — good
- ⚠️ 40–50 characters — borderline; flag as Minor and suggest shortening
- ❌ Over 50 characters — flag as Invalid; almost certainly truncated in the UI

---

## Workflow

### Step 1 — Establish separator

If the user hasn't told you which separator they use, ask before fetching pages. Check if a feature naming convention is already established — ideally pages and features share the same separator for visual consistency.

### Step 2 — Fetch pages via MCP

Use the Pendo MCP `searchEntities` tool to retrieve pages. Example call:

```
tool: searchEntities
entity_type: Page
```

This returns page metadata including `id`, `name`, `appId`, `group` (Product Area), `createdAt`, `lastUpdatedAt`, `createdByUser`, and `lastUpdatedByUser`.

Use the page `id` to construct a direct link to the page in Pendo:
```
https://app.pendo.io/analytics/page/{pageId}
```

> **Note:** If `searchEntities` does not return `lastUpdatedAt`, `createdByUser`, or `lastUpdatedByUser` fields, fall back to the Aggregation API using a `pages` source pipeline. When author data is unavailable, show `—` in those columns.

### Step 3 — Apply filters

Default to **recently updated pages** unless the user specifies otherwise. Always ask the user to confirm or adjust the time window.

| Filter | Default | User can specify |
|---|---|---|
| Recently updated | Last 30 days | Number of days, or a specific date (e.g. "since Jan 1") |
| Recently created | Last 30 days | Number of days, or a specific date |
| By Product Area | — | Area name (from `group` field) |
| By App | — | App ID or name |
| By Author | — | Username from `createdByUser` |

When prompting for the time window, accept natural language:
- "last 7 days" → `lastUpdatedAt >= now - 7d`
- "since March 1" → `lastUpdatedAt >= 2025-03-01`
- "this month" → start of current calendar month

Apply date filters client-side after fetching, or push into the Aggregation API pipeline with a `filter` stage if using that fallback.

### Step 4 — Evaluate names

For each page name:

1. Detect the separator (confirm it matches what the user specified)
2. Split into segments
3. Apply segment rules and length rule
4. Classify:
   - ✅ **Valid** — fully matches the convention and under 40 chars
   - ⚠️ **Minor** — close but fixable (wrong case, borderline length, view starts with verb, mixed separators, unrecognized but plausible view type)
   - ❌ **Invalid** — wrong structure, missing segments, raw URL, view starts with a clear action verb, or over 50 chars

**Special check — verb-first View segment:** If the last segment starts with a recognized UI action verb (Edit, Create, Delete, Save, etc.), flag it as ❌ Invalid with the note: "View segment starts with a verb — this looks like a feature, not a page. Rename the view or re-tag as a feature."

### Step 5 — Report results

**Keep feedback concise.** Only describe what is wrong — do not comment on valid names.

**Summary block** (always show):
```
Audited: 38 pages  |  ✅ Valid: 22  |  ⚠️ Minor: 8  |  ❌ Invalid: 8
Filter: Updated in last 30 days
```

**Issues table** (⚠️ and ❌ only):

Hyperlink each page name to its Pendo page using `https://app.pendo.io/analytics/page/{id}`. Format the name as a markdown link: `[Page Name](url)`.

| Page Name | Status | Issue | Author | Last Updated By |
|---|---|---|---|---|
| [settings billing](https://app.pendo.io/analytics/page/abc123) | ❌ | No separators — cannot determine segments | jane@acme.com | — |
| [Analytics > Report](https://app.pendo.io/analytics/page/def456) | ❌ | Only one separator — missing Section segment | bob@acme.com | alice@acme.com |
| [Analytics > Funnels > edit funnel](https://app.pendo.io/analytics/page/ghi789) | ❌ | View segment starts with a verb ("edit") — looks like a feature, not a page | — | jane@acme.com |
| [Analytics > Funnels > report](https://app.pendo.io/analytics/page/jkl012) | ⚠️ | View not in Title Case | bob@acme.com | bob@acme.com |
| [Analytics - Funnels > Report](https://app.pendo.io/analytics/page/mno345) | ⚠️ | Mixed separators (`-` and `>`) | alice@acme.com | — |
| [/app/analytics/funnels/report](https://app.pendo.io/analytics/page/pqr678) | ❌ | Raw URL path — unreadable in dropdowns | — | — |

> ⚠️ **Name length:** Pendo truncates page names at approximately **40 characters** in most analytics dropdowns, reports, and dashboard widgets. Names over 40 chars risk the most specific segment (the View) being hidden from users. Names over 50 chars are flagged ❌ Invalid.

**Do not list valid pages** unless the user explicitly asks.

### Step 6 — Recommend next steps

After the report, recommend actions the user can take — but **do not offer to make corrections yourself**. The user owns their page taxonomy.

Suggested recommendations to offer:
- Review invalid pages in Pendo's Pages List and rename them directly in the UI
- Check if any verb-first pages should be re-tagged as features instead
- Share the issues table with your team so the right owners can fix their pages
- Set up a naming review as part of your page tagging process going forward
- Re-run this audit after fixes to confirm compliance
- Consider auditing another product area or time window next

---

## Recognized view type words (reference)

These are words that commonly and appropriately end a page View segment. Not required, but their presence is a positive signal that the name describes a screen rather than an action.

Overview, List, Details, Settings, Dashboard, Report, Profile, Summary,
Home, Feed, Index, Gallery, Grid, Table, Calendar, Timeline, History,
Wizard, Modal, Panel, Drawer, Sidebar, Banner, Form, Page, Screen,
Directory, Library, Catalog, Queue, Inbox, Archive, Preview, Review,
Builder, Editor, Viewer, Picker, Selector, Chooser, Manager, Explorer

If the View segment does not use one of these words but is still clearly a noun phrase describing a screen (e.g. `Company Info`, `Team Members`, `Billing Address`), that is ✅ acceptable — the list is a guide, not a requirement.

---

## Edge cases

- **Null / empty names** — ❌ Invalid: "Name is empty"
- **Raw URL paths** (e.g. `/app/settings`) — ❌ Invalid: "Raw URL path — rename to a human-readable label"
- **Auto-tagged names with query params** (e.g. `My App - /?modal=true`) — ❌ Invalid: "Auto-tagged URL pattern — rename or consolidate"
- **All-caps segments** (e.g. `ANALYTICS`) — ⚠️ Minor: suggest Title Case
- **Trailing separator** (e.g. `Analytics > Funnels >`) — ❌ Invalid: empty final segment
- **Underscore or space-only separator** — ⚠️ Minor: not recommended, suggest `>`, `-`, or `|`
- **Numeric-only segments** — ❌ Invalid
- **View starts with action verb** — ❌ Invalid: "looks like a feature, not a page"
- **Over 4 segments** — ⚠️ Minor only if total length is still under 40 chars; ❌ Invalid if over 50 chars