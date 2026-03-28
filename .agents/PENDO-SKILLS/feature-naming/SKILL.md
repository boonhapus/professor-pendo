---
name: feature-naming
description: >
  Audits Pendo feature names against a naming convention template to improve
  discoverability in analytics dropdowns. Use this skill whenever the user wants
  to check, audit, review, or validate Pendo feature names — including requests
  like "check my Pendo feature naming", "audit feature names", "which features
  don't follow the naming convention", "review my recently updated features", or
  "help me find badly named features". Always trigger this skill when the user
  mentions Pendo features AND naming, conventions, consistency, or discoverability,
  even if they phrase it casually.
---

# feature-naming

Audits Pendo feature names against a naming convention and explains why consistent naming matters.

---

## Why naming conventions matter

Consistent feature naming is one of the highest-leverage things a Pendo admin can do. Features appear as raw names in:
- **Analytics dropdowns** — Feature Adoption, Path, Funnel, and Retention reports
- **Dashboard widgets** — where names are the only label shown
- **Tagged element lists** — used by non-technical stakeholders

A good naming convention makes features instantly scannable. A bad one forces users to mentally decode what `btn_save_2_FINAL` or `Homepage Click` actually means — and they often just give up and pick the wrong one.

**Keep names short:** The Pendo UI truncates feature names at approximately **40 characters** in most dropdowns and name fields. The most specific segment — usually the Action Element — is the part most likely to be cut off. Aim to stay under 40 characters.

---

## Naming convention

The structure reads naturally as: *"the action element is in the area, on the page."*

> **`[Page] [sep] [Area] [sep] [Action Element]`**
>
> Examples using `>` as separator:
> - `Payment Settings > Billing > Edit Method`
> - `Company Setup > Onboarding > Submit Form`
> - `Overview > Dashboard > Filter Date Range`

### Separator

The user chooses their own separator. Ask at the start of an audit if no separator has been established.

| Separator | Example | Notes |
|---|---|---|
| `>` | `Overview > Dashboard > Filter` | Clear, readable, widely used |
| `-` | `Overview - Dashboard - Filter` | Clean, minimal |
| `\|` | `Overview \| Dashboard \| Filter` | High contrast in dropdowns |

**Not recommended:**
- `_` (underscore) — hard to read, looks like a code artifact
- space only — ambiguous, no clear segment boundaries

The separator must be used **consistently** across all segments in a name. Mixed separators within a single name are a ⚠️ Minor issue.

### Segment rules

0. **Segment 0 (App Name) — optional** — Some teams prefix all feature names with the app name (e.g. `MyApp > Payment Settings > Billing > Edit Method`). This is acceptable as long as it is used **consistently across all features in that app**. If the app name is longer than ~8 characters, flag a ⚠️ warning that it will consume a significant portion of the 40-character limit, leaving less room for the meaningful segments.
1. **Segment 1 (Page)** — Title Case, 1–4 words
2. **Segment 2 (Area)** — Title Case, 1–3 words
3. **Segment 3+ (Action Element)** — verb + noun(s) in Title Case; verb must be a recognized UI action word (see reference list below). Additional segments beyond 3 are allowed if needed for specificity, but the **total name length must stay under 40 characters**.
4. Each segment must be non-empty after trimming
5. No double spaces, no leading/trailing spaces per segment

When evaluating consistency of the app name prefix: if some features in the same app include the app name segment and others don't, flag the inconsistent ones as ⚠️ Minor.

### Length rule

- ✅ Under 40 characters — good
- ⚠️ 40–50 characters — borderline; flag as Minor and suggest shortening
- ❌ Over 50 characters — flag as Invalid; almost certainly truncated in the UI

---

## Workflow

### Step 1 — Establish separator

If the user hasn't told you which separator they use, ask before fetching features. This is needed to correctly split and evaluate names.

### Step 2 — Fetch features via MCP

Use the Pendo MCP `searchEntities` tool to retrieve features. Example call:

```
tool: searchEntities
entity_type: Feature
```

This returns feature metadata including `id`, `name`, `appId`, `group` (Product Area), `createdAt`, `lastUpdatedAt`, `createdByUser`, and `lastUpdatedByUser`.

Use the feature `id`, the subscription ID, and the correct app **domain for the data environment** to build the feature URL:
```
https://{domain}/s/{subscriptionId}/features/{featureId}
```

`{domain}` follows `PENDO_DATA_ENVIRONMENT` (same hosts as the Pendo app / API): `io` → `app.pendo.io`, `eu` → `app.eu.pendo.io`, `us1` → `us1.app.pendo.io`, `jpn` → `app.jpn.pendo.io`, `au` → `app.au.pendo.io`.

> **Note:** If `searchEntities` does not return `lastUpdatedAt`, `createdByUser`, or `lastUpdatedByUser` fields, fall back to the Aggregation API (see the `get-pendo-features` skill for the query pattern). When author data is unavailable, show `—` in those columns.

### Step 3 — Apply filters

Default to **recently updated features** unless the user specifies otherwise. Always ask the user to confirm or adjust the time window.

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

For each feature name:

1. Detect the separator (confirm it matches what the user specified)
2. Split into segments
3. Apply segment rules and length rule
4. Classify:
   - ✅ **Valid** — fully matches the convention and under 40 chars
   - ⚠️ **Minor** — close but fixable (wrong case, borderline length, near-match verb, mixed separators)
   - ❌ **Invalid** — wrong structure, missing segments, unrecognized action verb, or over 50 chars

### Step 5 — Report results

**Keep feedback concise.** Only describe what is wrong — do not comment on valid names.

**Summary block** (always show):
```
Audited: 42 features  |  ✅ Valid: 28  |  ⚠️ Minor: 6  |  ❌ Invalid: 8
Filter: Updated in last 30 days
```

**Issues table** (⚠️ and ❌ only):

Hyperlink each feature name using `https://{domain}/s/{subscriptionId}/features/{id}` (see Step 2 for `{domain}`). Format the name as a markdown link: `[Feature Name](url)`.

| Feature Name | Status | Issue | Author | Last Updated By |
|---|---|---|---|---|
| [billing edit](https://app.pendo.io/s/123456/features/abc123) | ❌ | No separators — cannot determine segments | jane@acme.com | — |
| [Payment Settings > Save](https://app.pendo.io/s/123456/features/def456) | ❌ | Only one separator — missing Area segment | bob@acme.com | alice@acme.com |
| [Payment Settings > Billing > save method](https://app.pendo.io/s/123456/features/ghi789) | ⚠️ | Action Element not in Title Case | — | jane@acme.com |
| [Payment Settings > Billing > Do the Thing](https://app.pendo.io/s/123456/features/jkl012) | ❌ | "Do" is not a recognized UI action verb | bob@acme.com | bob@acme.com |
| [Payment Settings - Billing > Edit Method](https://app.pendo.io/s/123456/features/mno345) | ⚠️ | Mixed separators (`-` and `>`) | alice@acme.com | — |

> ⚠️ **Name length:** Pendo truncates feature names at approximately **40 characters** in most analytics dropdowns, reports, and dashboard widgets. Names over 40 chars risk the most specific segment being hidden from users. Names over 50 chars are flagged ❌ Invalid.

**Do not list valid features** unless the user explicitly asks.

### Step 6 — Recommend next steps

After the report, recommend actions the user can take — but **do not offer to make corrections yourself**. The user owns their feature taxonomy.

Suggested recommendations to offer:
- Review the invalid features in Pendo's Feature List and rename them directly in the UI
- Share the issues table with your team so the right owners can fix their features
- Set up a naming review as part of your feature tagging process going forward
- Re-run this audit after fixes to confirm compliance
- Consider auditing another product area or time window next

---

## Recognized UI action verbs (reference)

Click, Submit, Filter, Open, Close, Edit, Delete, Toggle, Upload, Download,
Select, View, Expand, Collapse, Search, Save, Cancel, Add, Remove, Create,
Update, Send, Copy, Share, Export, Import, Sort, Refresh, Reset, Navigate,
Launch, Enable, Disable, Approve, Reject, Assign, Archive, Restore, Preview,
Confirm, Dismiss, Skip, Complete, Start, Stop, Pause, Resume, Schedule, Tag,
Comment, React, Pin, Unpin, Follow, Unfollow, Mark, Unmark, Lock, Unlock

If an action word is close but not listed (e.g. "Modify" instead of "Edit"),
flag as ⚠️ Minor and note the closest recognized verb.

---

## Edge cases

- **Null / empty names** — ❌ Invalid: "Name is empty"
- **All-caps segments** (e.g. `BILLING`) — ⚠️ Minor: suggest Title Case
- **Trailing separator** (e.g. `Page > Area >`) — ❌ Invalid: empty final segment
- **Underscore or space-only separator** — ⚠️ Minor: not recommended, suggest `>`, `-`, or `|`
- **Numeric-only segments** — ❌ Invalid
- **Over 4 segments** — ⚠️ Minor only if total length is still under 40 chars; ❌ Invalid if over 50 chars