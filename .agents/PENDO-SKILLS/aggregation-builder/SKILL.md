---
name: aggregation-builder
description: >-
  Use this skill when the user wants to query Pendo data using the Aggregation
  API. Triggers: any request to count, list, filter, group, trend, or analyze
  Pendo visitors, accounts, events, pages, features, guides, polls, or track
  events. Also triggers on: 'write me an aggregation', 'how many visitors',
  'show me usage', 'build a query', 'top pages', 'active users', 'retention',
  'funnel', or any natural-language analytics question about Pendo product
  data. Do NOT use for Pendo SDK installation, metadata write APIs, or SCIM
  provisioning.
metadata:
  version: "0.1.0"
---

# Pendo Aggregation Builder

## What This Skill Does

Translates natural-language analytics questions into runnable Pendo Aggregation API queries (JSON). The workflow is: **classify intent → clarify missing details → load only the references needed → compose and return a query**.

## Step 1: Classify the User's Intent

Read the user's request and assign it to one or more of these intent categories:

| Intent | Signal words / patterns | References to load |
|--------|------------------------|--------------------|
| **List / Export** | "list visitors", "export accounts", "show me all…" | sources |
| **Count / Metric** | "how many", "total", "count of" | sources, aggregators |
| **Trend / Time Series** | "per day", "over time", "daily", "weekly trend" | sources (timeSeries), aggregators |
| **Top-N / Ranking** | "top 10", "most active", "highest", "ranked by" | sources, operators, aggregators |
| **Breakdown / Group-by** | "by account", "per OS", "grouped by language" | sources, operators, aggregators |
| **Enrichment** | "with visitor name", "include metadata", "add account info" | operators (bulkExpand/merge) |
| **Funnel / Path** | "funnel", "conversion", "path from X to Y" | operators, aggregators (funnel/path) |
| **Retention / Cohort** | "retention", "cohort", "returning users" | sources (timespan), operators (retention) |
| **Segment** | "in segment X", "only enterprise users" | operators (segment) |
| **Filter-heavy** | "where X > Y", "excluding Z", "only identified" | operators (filter) |

Most real questions combine 2–3 intents (e.g., "Top 10 visitors by events, grouped by account, over the last 30 days" = Top-N + Breakdown + Trend).

## Step 2: Clarify Missing Details

Before composing a query, you need these details. Ask about any that are missing or ambiguous. **Collect all missing details in a single clarification turn** — don't ask one at a time.

### Always Required
- [ ] **Entity**: What are we counting/listing? (visitors, accounts, events, pages, features, guides)
- [ ] **Time range**: Over what period? (last 7/30/90 days, specific dates, all time for non-event sources)
- [ ] **Metric**: What are we measuring? (count, sum of events, minutes active, days active, etc.)

### Often Required (ask if ambiguous)
- [ ] **Granularity**: One total, or broken out per day/week/month? (aggregate vs. iterative)
- [ ] **App scope**: Specific app ID, or all apps? (single-app subs can skip this)
- [ ] **Identified only?**: Exclude anonymous `_PENDO_T_` visitors? (almost always yes)
- [ ] **Filters**: Any conditions? (specific page, feature, account, visitor attribute, segment)
- [ ] **Sorting / Limit**: Top-N? Sorted by what?
- [ ] **Enrichment**: Need visitor/account names or other metadata in the output?

### Occasionally Required
- [ ] **Blacklist**: Apply, ignore, or only blacklisted? (default: apply)
- [ ] **Output format**: JSON or CSV? (default: JSON)
- [ ] **Segment**: By ID or by inline rules?

## Step 3: Load References

Based on the intent classification, read **only** the references you need. Do NOT load everything.

| If you need to… | Load this file |
|-----------------|----------------|
| Choose a source, configure timeSeries, understand available fields | `references/sources-and-timeseries.md` |
| Use any pipeline operator (filter, group, sort, merge, fork, etc.) | `references/operators.md` |
| Use field aggregators (count, sum, avg, etc.) or write expressions | `references/aggregators-and-expressions.md` |
| See full worked examples for common patterns | `references/examples.md` |

**Minimum load for any query:** `sources-and-timeseries.md` (you always need a source).

**Common load sets:**
- Simple list/export → sources only
- Count or metric → sources + aggregators
- Top-N with grouping → sources + operators + aggregators
- Complex multi-step → sources + operators + aggregators + examples

## Step 4: Compose the Query

### Query Skeleton

Every aggregation follows this structure:

```json
{
  "response": {
    "location": "request",
    "mimeType": "application/json"
  },
  "request": {
    "requestId": "<descriptive-id>",
    "pipeline": [
      { "source": { "<source>": { ... }, "timeSeries": { ... } } },
      // ... operators ...
    ]
  }
}
```

### Composition Order (follow this sequence)

1. **Source** — Pick the right source for the entity and add timeSeries if needed
2. **Early filters** — `identified`, `filter`, `segment` (reduce rows before expensive ops)
3. **Transform** — `eval`, `select`, `set` (compute/rename fields)
4. **Group / Reduce** — Aggregate data per key or across all rows
5. **Enrich** — `bulkExpand`, `merge`, `expand` (add metadata AFTER reducing row count)
6. **Post-group operations** — Additional `group`, `filter`, `select` on aggregated data
7. **Sort + Limit** — Order and cap results

### API Endpoint

```
POST https://app.pendo.io/api/v1/aggregation
Headers:
  x-pendo-integration-key: <KEY>
  Content-Type: application/json
```

## Step 5: Return the Query

Present the final JSON query with:
1. A brief explanation of what each pipeline step does (as comments or a short list)
2. Any caveats (e.g., "this uses `daily` so you'll get one result per day")
3. Placeholders marked clearly: `<YOUR_APP_ID>`, `<YOUR_PAGE_ID>`, etc.

---

## Quick Decision Trees

### Which source do I need?

```
Need visitor metadata only?          → visitors
Need account metadata only?          → accounts
Need event counts (pre-aggregated)?  → events (page+feature), pageEvents, featureEvents, trackEvents
Need individual raw events?          → singleEvents
Need guide interactions?             → guideEvents
Need poll responses?                 → pollEvents
Need activity bitmaps (days active)? → timespan
Need page/feature definitions?       → pages, features
Need guide definitions?              → guides
```

### Aggregate or iterative period?

```
"Total over the range" (one number)   → dayRange / weekRange / monthRange
"Per day/week/month" (one per period) → daily / weekly / monthly
```

### Which aggregator for my metric?

```
"How many unique X"     → count: "field"
"How many rows"         → count: null
"Total of X"            → sum: "field"
"Average X"             → avg: "field"
"Highest / lowest X"    → max / min: "field"
"X per day trend"       → use iterative period + count/sum
"Days active"           → daysActiveCreate + daysActiveCount (from events)
                          or daysActiveUnion + daysActiveCount (from timespan)
"Retention"             → retention operator with timespan source
```
