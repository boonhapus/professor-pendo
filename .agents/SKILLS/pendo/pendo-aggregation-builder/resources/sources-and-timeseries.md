# Sources & Time Series Reference

## Source Catalog

### Event Sources (require `timeSeries`)

| Source | Description | Row Granularity | Key Fields |
|--------|-------------|-----------------|------------|
| `events` | Pre-aggregated page + feature events | 1 row per visitor/page/day/account/IP/server combo | `visitorId`, `accountId`, `appId`, `pageId`, `day`, `numEvents`, `numMinutes`, `userAgent`, `server`, `remoteIp`, `parameters` |
| `pageEvents` | Pre-aggregated page events only | Same as `events` but page-only | Same as `events` |
| `featureEvents` | Pre-aggregated feature events only | Same as `events` but feature-only | Same as `events` plus `featureId` |
| `trackEvents` | Pre-aggregated track type events | Same as `events` | Same as `events` plus `trackTypeId` |
| `guideEvents` | Guide interaction events | 1 row per guide event | `visitorId`, `accountId`, `appId`, `guideId`, `guideStepId`, `type`, `browserTime` |
| `pollEvents` | Poll response events | 1 row per poll response | `visitorId`, `accountId`, `guideId`, `pollId`, `pollResponse` |
| `singleEvents` | Individual un-aggregated events | 1 row per raw event | `visitorId`, `accountId`, `appId`, `browserTime`, `type`, `url`, `elementPath`, `eventId`, `tabId`, `country`, `region`, `latitude`, `longitude` |
| `rawEvents` | Lowest-level raw events | 1 row per raw event | Similar to `singleEvents` |

### Metadata Sources (no `timeSeries`)

| Source | Description | Key Fields |
|--------|-------------|------------|
| `visitors` | All visitors with metadata | `visitorId`, `metadata.auto.*` (firstvisit, lastvisit, lastbrowsername, etc.), `metadata.agent.*` (custom agent fields) |
| `accounts` | All accounts with metadata | `accountId`, `metadata.auto.*`, `metadata.agent.*` |
| `pages` | Page definitions | `pageId`, `name`, `rules`, `appId` |
| `features` | Feature definitions | `featureId`, `name`, `rules`, `appId` |
| `trackTypes` | Track type definitions | `trackTypeId`, `name`, `appId` |
| `guides` | Guide definitions | `guideId`, `name`, `steps`, `appId` |
| `apps` | Application definitions | `appId`, `name` |

### Special Sources

| Source | Description | Key Fields |
|--------|-------------|------------|
| `timespan` | Visitor/account activity summary with activeDays bitmaps | `visitorId`, `accountId`, `appId`, `activeDays`, `firstTime`, `lastTime` |
| `guidesSeenEver` | All-time guide view data | `visitorId`, `guideId` |
| `pollsSeenEver` | All-time poll response data | `visitorId`, `pollId` |
| `const` | Inline constant rows for testing | User-defined |

### Source Syntax

```json
// Event source with timeSeries
{ "source": {
    "events": { "appId": -323232, "blacklist": "apply" },
    "timeSeries": { "period": "dayRange", "first": "now()", "count": -30 }
} }

// Metadata source (no timeSeries)
{ "source": { "visitors": null } }

// Source with all apps
{ "source": { "events": { "appId": "expandAppIds(\"*\")" }, "timeSeries": { ... } } }

// Constant source for testing
{ "source": { "const": [{"name": "Alice", "score": 90}, {"name": "Bob", "score": 75}] } }

// Timespan source (has its own appId param, not timeSeries)
{ "source": { "timespan": { "kind": "visitor", "appId": "expandAppIds(\"*\")" } } }
```

### Source Parameters

**`appId`** — Scope to specific app(s):
- Single app: `"appId": -323232`
- Multiple apps: `"appId": [-323232, 64324839843]`
- All apps: `"appId": "expandAppIds(\"*\")"`

**`blacklist`** — Exclude-list behavior:
- `"apply"` (default): Exclude blacklisted activity
- `"ignore"`: Include everything
- `"only"`: Return only blacklisted activity

---

## Time Series Configuration

### Structure

```json
"timeSeries": {
  "period": "<period>",
  "first": "<timestamp or expression>",
  "last": "<timestamp or expression>"   // OR "count": <integer>
}
```

### Periods

| Time Unit | Aggregate (one result total) | Iterative (one result per period) |
|-----------|------------------------------|-----------------------------------|
| Hour      | `hourRange`                  | `hourly`                           |
| Day       | `dayRange`                   | `daily`                            |
| Week (Sun-aligned) | `weekRange`          | `weekly`                           |
| Month (1st-aligned) | `monthRange`        | `monthly`                          |

**Rule of thumb:**
- Use `...Range` when you want a single answer across the whole window
- Use `...ly` when you want separate answers per period (charts, trends)

### Time Range Patterns

```json
// Last 30 days (most common)
{ "period": "dayRange", "first": "now()", "count": -30 }

// Specific date range
{ "period": "dayRange", "first": "date(2024,1,1)", "last": "date(2024,3,31)" }

// Last 7 days, one result per day (for charts)
{ "period": "daily", "first": "now()", "count": -7 }

// Last 1 hour
{ "period": "hourRange", "first": "now()", "count": -1 }

// Last 6 months, one result per month
{ "period": "monthly", "first": "now()", "count": -6 }

// Forward from a date (3 days starting Jan 1)
{ "period": "dayRange", "first": "date(2024,1,1)", "count": 3 }
```

### How `count` Works

- **Positive count**: Start at `first`, span forward N periods
- **Negative count**: End just *before* the period containing `first`, span backward |N| periods
  - `"first": "now()", "count": -30` → the 30 days ending yesterday (today excluded)

### Timestamp Expressions for `first` / `last`

| Expression | Result |
|-----------|--------|
| `now()` | Current server time |
| `date("2024-01-15")` | Jan 15 2024 midnight (subscription TZ) |
| `date(2024, 1, 15)` | Same, integer form |
| `date(2024, 1)` | Jan 1 2024 midnight |
| `startOfPeriod("monthly", now())` | Start of current month |
| `dateAdd(now(), -90, "days")` | 90 days ago |

Expressions can be nested:
```json
"first": "startOfPeriod(\"monthly\", dateAdd(now(), -6, \"months\"))"
```

### Timezone Rules

- All timestamps are millisecond Unix timestamps (no timezone).
- All date math uses the **subscription's timezone**.
- Always use `date()` to construct timestamps — never browser-local conversion.
- Prefer `date()` over raw millisecond literals for readability and correctness.
