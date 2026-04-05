# Pipeline Operators Reference

Operators transform rows as they flow through the pipeline. Each step receives rows from the step above and outputs rows to the step below. **Order matters.**

---

## Basic Operators

### `limit` — Cap row count

```json
{ "limit": 10 }
```

Always use during development. Place after `sort` for Top-N queries. A `limit` immediately after `group` triggers a performance optimization (but sort order is not guaranteed).

### `filter` — Keep matching rows

```json
{ "filter": "<expression>" }
```

Examples:
```json
{ "filter": "numEvents > 10" }
{ "filter": "accountId != \"\"" }
{ "filter": "contains(visitorId, \"@pendo.io\")" }
{ "filter": "len(accountId) >= 10" }
{ "filter": "!isNull(parameters.setting) && parameters.setting != \"\"" }
```

### `identified` — Keep only identified visitors

```json
{ "identified": "visitorId" }    // Keep identified only
{ "identified": "!visitorId" }   // Keep anonymous only
```

Filters out `_PENDO_T_*` anonymous IDs. Prefer this over a manual `filter` — it's performance-optimized.

### `select` — Keep and rename fields (drops all others)

```json
{
  "select": {
    "visitor": "visitorId",
    "eventCount": "numEvents",
    "eventsPerMin": "numEvents / numMinutes"
  }
}
```

### `eval` — Add or replace fields (keeps all others)

```json
{ "eval": { "eventsPerMinute": "numEvents / numMinutes" } }
```

Multiple fields in one `eval` execute in **undefined order**. If field B depends on field A, use two steps:
```json
{ "eval": { "rate": "numEvents / numMinutes" } },
{ "eval": { "kiloRate": "rate / 1000" } }
```

### `set` — Set field to constant

```json
{ "set": { "status": "active" } }
```

### `sort` — Order rows

```json
{ "sort": ["fieldName"] }          // Ascending
{ "sort": ["-fieldName"] }         // Descending
{ "sort": ["-numEvents", "visitorId"] }  // Multi-field
```

### `count` — Count all rows

```json
{ "count": null }
```

Replaces all rows with a single `{"count": N}`. For counting unique values, use the `count` **aggregator** inside `reduce` or `group` instead.

### `reduce` — Collapse all rows into one

```json
{
  "reduce": {
    "totalVisitors": { "count": "visitorId" },
    "totalEvents": { "sum": "numEvents" },
    "earliest": { "min": "day" }
  }
}
```

Uses field aggregators (see `aggregators-and-expressions.md`).

### `group` — Group rows and aggregate per group

```json
{
  "group": {
    "group": ["visitorId", "accountId"],
    "fields": [
      { "totalMinutes": { "sum": "numMinutes" } },
      { "rowCount": { "count": null } }
    ]
  }
}
```

Group with no aggregators returns unique combinations:
```json
{ "group": { "group": ["visitorId", "accountId"] } }
```

**`forceKeys`** — Guarantee specific groups in output (even if empty):
```json
{
  "group": {
    "group": ["status"],
    "fields": [{ "n": { "count": null } }],
    "forceKeys": { "status": "list(\"active\",\"churned\",\"trial\")" }
  }
}
```
Output will include rows for all three statuses; missing ones get zero-valued aggregators.

### `cat` — Pass-through (no-op)

```json
{ "cat": null }
```

Useful only as a placeholder inside `fork` or `merge` pipelines.

---

## Advanced Operators

### `bulkExpand` — Enrich with visitor/account metadata

```json
{ "bulkExpand": { "visitorInfo": { "visitor": "visitorId" } } }
{ "bulkExpand": { "accountInfo": { "account": "accountId" } } }
```

Adds a nested object (e.g., `visitorInfo.auto.firstvisit`, `visitorInfo.agent.email`) to each row by looking up the visitor/account journal.

**Performance:** Always filter/group/limit rows *before* bulkExpand. Expanding millions of rows is expensive. Also, limiting the events source to < 30 days avoids loading the cutoff journal.

### `expand` — Enrich with entity metadata

```json
{ "expand": { "pageInfo": { "page": "pageId" } } }
```

Works with: `pageId`, `featureId`, `trackTypeId`, `accountId`, `visitorId`, `vocItemId`. Use `bulkExpand` instead for visitor/account — it's optimized for large sets.

### `expandList` — Expand array of IDs to metadata

```json
{
  "expandList": {
    "inputField": "productAreaIds",
    "outputField": "productAreas",
    "typeName": "productArea"
  }
}
```

Supports: `productArea`, `label`, `app`, `vocInsight`.

### `segment` — Filter by segment membership

```json
// By existing segment ID
{ "segment": { "id": "<segmentId>" } }

// With inline rules
{ "segment": {
    "source": {
      "visitors": null
    },
    "filter": "metadata.agent.plan == \"enterprise\""
} }
```

### `merge` — Join data from an inner pipeline

```json
{
  "merge": {
    "fields": ["visitorId"],
    "mappings": { "name": "metadata.agent.firstname" },
    "pipeline": [
      { "source": { "visitors": null } },
      { "cat": null }
    ]
  }
}
```

1. Runs the inner pipeline to produce merge rows
2. Matches on `fields` keys
3. Copies values per `mappings` into main rows

If `mappings` is omitted, all inner-pipeline fields are copied over.

### `spawn` — Combine multiple sources

```json
{
  "spawn": [
    [{ "source": { "events": { "appId": -323232 } },
       "timeSeries": { "period": "hourRange", "first": "now()", "count": -1 } }],
    [{ "source": { "events": { "appId": 99999 } },
       "timeSeries": { "period": "hourRange", "first": "now()", "count": -1 } }]
  ]
}
```

Each inner pipeline must have its own source. Rows from all branches are combined into one stream. Cannot use iterative periods.

### `fork` — Send rows to parallel sub-pipelines

```json
{
  "fork": [
    [{ "group": { "group": ["visitorId"], "fields": [{ "time": { "sum": "numMinutes" } }] } }],
    [{ "group": { "group": ["accountId"], "fields": [{ "time": { "sum": "numMinutes" } }] } }]
  ]
}
```

Every row goes to every fork. Results from all forks are combined and continue down the pipeline. Empty pipelines are not allowed (use `cat` for pass-through). Often combined with `join`.

### `join` — Merge forked/spawned rows by key

```json
{
  "join": {
    "fields": ["visitorId"],
    "width": 2
  }
}
```

`width` = how many rows per key to expect before emitting a merged result.

### `unwind` — Expand array into rows

```json
{
  "unwind": {
    "field": "items",
    "index": "itemIndex",
    "keepEmpty": false,
    "prefix": false
  }
}
```

| Parameter | Description |
|-----------|-------------|
| `field` | Array field to expand |
| `index` | (optional) Store element index in this field |
| `keepEmpty` | `true` = preserve rows where array is null/empty |
| `prefix` | `true` = emit prefix slices instead of individual elements |

### `itemSeen` — All-time usage data for a countable

```json
{
  "itemSeen": {
    "usageData": { "pageId": "<page-id>" }
  }
}
```

Appends `{ "lastUsed": <ts>, "count": <n> }` per visitor for the given page/feature/trackType. Ignores blacklist.

### `useragent` — Parse user agent string

```json
{ "useragent": { "userAgent": "userAgent" } }
```

Produces: `userAgent.os`, `userAgent.browser`, `userAgent.version`, etc.

### `pages` / `features` — Match URLs/elements to countables

```json
{ "pages": { "pageIds": "url" } }
{ "features": { "featureIds": "elementPath" } }
```

Appends an array of matching page/feature IDs to each row.

### `matchRules` — Test against page/feature rules

**Field mode** (adds boolean):
```json
{ "matchRules": { "entity": "Page", "field": "match", "rules": ["//*/path"], "rulesType": "web" } }
```

**Filter mode** (drops non-matches):
```json
{ "matchRules": { "entity": "Page", "filter": true, "rules": ["//*/path"], "rulesType": "web" } }
```

Works with `"entity": "Page"` (matches on `url`) and `"entity": "Feature"` (matches on `url` + `elementPath`).

### `retention` — Cohort retention analysis

```json
{
  "retention": {
    "timeSeries": { "period": "monthRange", "first": "date(2024,7,1)", "count": 6 },
    "offset": 30,
    "cohortField": "cohort",
    "relativePeriodsField": "relativePeriod",
    "cohortMode": "first"
  }
}
```

Only works with `timespan` source. `cohortMode`:
- `"first"`: Visitors grouped into cohort of their first activity
- `"all"`: Visitors in every cohort where they had activity
