# Field Aggregators & Expressions Reference

## Field Aggregators

Aggregators are used inside `group.fields` and `reduce` to produce a single value per group (or across all rows).

### Syntax

```json
// Inside reduce (all rows → one row)
{ "reduce": { "outputFieldName": { "<aggregator>": "<expression or null>" } } }

// Inside group (per-group aggregation)
{ "group": {
    "group": ["groupField"],
    "fields": [{ "outputFieldName": { "<aggregator>": "<expression or null>" } }]
} }
```

### Complete Aggregator List

#### Counting

| Aggregator | Syntax | Description |
|-----------|--------|-------------|
| `count` (rows) | `{"count": null}` | Count total rows |
| `count` (unique) | `{"count": "field"}` | Count unique values of one field |
| `count` (unique combo) | `{"count": ["f1","f2"]}` | Count unique value pairs |
| `countIf` | `{"countIf": {"count": "field", "if": "expr"}}` | Count unique values where condition is true |

**`count: null` vs. `count: "field"`**: On pre-aggregated sources (events, pageEvents), one visitor can have multiple rows (different day/account/IP combos). `count: null` counts rows; `count: "visitorId"` counts unique visitors. After a `group` on `visitorId`, they're equal.

**countIf example:**
```json
{ "reduce": {
    "anonymousCount": { "countIf": { "count": "visitorId", "if": "startsWith(visitorId, `_PENDO_T_`)" } }
} }
```

#### Numeric Aggregation

| Aggregator | Syntax | Description |
|-----------|--------|-------------|
| `sum` | `{"sum": "expr"}` | Sum of values |
| `avg` | `{"avg": "expr"}` | Average |
| `mean` | `{"mean": "expr"}` | Average (alias) |
| `min` | `{"min": "expr"}` | Minimum |
| `max` | `{"max": "expr"}` | Maximum |
| `median` | `{"median": "expr"}` | Median |
| `stddev` | `{"stddev": "expr"}` | Standard deviation |
| `var` | `{"var": "expr"}` | Variance |

All accept expressions: `{"sum": "numEvents * 100"}`, `{"avg": "numEvents / numMinutes"}`.

#### Collection

| Aggregator | Syntax | Description |
|-----------|--------|-------------|
| `first` | `{"first": "expr"}` | First non-null value received |
| `list` | `{"list": "expr"}` | Collect all values into an array |
| `listIf` | `{"listIf": {"list": "expr", "if": "expr"}}` | Collect values where condition is true |
| `listAverage` | `{"listAverage": "expr"}` | Average of a list field |
| `concat` | `{"concat": "expr"}` | Merge/flatten arrays together |

**Caution with `first`**: The value depends on the order rows arrive. Sort before reducing if you need a deterministic "first."

#### Percentiles

```json
{ "reduce": {
    "distribution": {
      "percentiles": {
        "field": "numEvents",
        "min": 0,
        "p25": 25,
        "median": 50,
        "p75": 75,
        "max": 100
      }
    }
} }
```

Keys are user-chosen names; values are percentile levels (0–100).

#### Activity Bitmaps

| Aggregator | Syntax | Description |
|-----------|--------|-------------|
| `daysActiveCreate` | `{"daysActiveCreate": "day"}` | Convert day timestamps into an activeDays bitmap |
| `daysActiveUnion` | `{"daysActiveUnion": "activeDays"}` | Merge multiple activeDays bitmaps |
| `daysActiveCount` | `{"daysActiveCount": {...}}` | Windowed time-series analysis on activeDays |
| `minutesActiveUnion` | `{"minutesActiveUnion": "minutesActive"}` | Merge minutesActive bitmaps |
| `minutesActiveCount` | `{"minutesActiveCount": "minutesActive"}` | Count minutes in a bitmap |

**daysActiveCount parameters:**
```json
{
  "daysActiveCount": {
    "field": "activeDays",
    "first": "date(2024,1,1)",
    "window": 30,
    "count": 12,
    "stride": 1,
    "stridePeriod": "monthly",
    "thresholds": { "count": 1 }
  }
}
```
- `window`: Days in each counting window
- `count`: Number of windows
- `stride` + `stridePeriod`: How far each window shifts
- `thresholds`: Activity levels (default `{"count": 1}` = any activity)

#### Sequence (Guide Sessions)

```json
{
  "sequence": {
    "new": "eventSubType(type) == \"guideSeen\"",
    "sort": ["browserTime"]
  }
}
```

Returns nested arrays grouped by the `new` expression; each sub-array sorted by `sort`. Used for guide activity analysis.

---

## Expressions

Expressions are used in `filter`, `eval`, `select`, aggregator parameters, and `timeSeries` fields. They follow C-like syntax.

### Operators

| Operator | Description |
|----------|-------------|
| `==`, `!=` | Equality |
| `>`, `<`, `>=`, `<=` | Comparison |
| `&&`, `\|\|`, `!` | Logic |
| `+`, `-`, `*`, `/`, `%` | Arithmetic |
| `()` | Grouping |

All numbers are floats internally.

### String Escaping

Strings inside JSON expressions require escaped quotes:
```json
{ "filter": "accountId == \"my-account\"" }
{ "filter": "startsWith(visitorId, `_PENDO_T_`)" }
```

### Common Functions

#### String Functions

| Function | Example | Description |
|----------|---------|-------------|
| `contains(s, sub)` | `contains(visitorId, "@pendo.io")` | Substring check |
| `startsWith(s, pre)` | `startsWith(visitorId, "_PENDO_T_")` | Prefix check |
| `len(s)` | `len(accountId)` | String/array length |
| `formatTime(fmt, ts)` | `formatTime("2006-01-02", day)` | Format timestamp (Go layout) |

#### Null / Conditional

| Function | Example | Description |
|----------|---------|-------------|
| `isNull(f)` | `isNull(accountId)` | True if field is null |
| `if(cond, then, else)` | `if(isNull(x), 0, x)` | Conditional |
| `identified(f)` | `identified(visitorId)` | True if not anonymous |

#### Date / Time

| Function | Example | Description |
|----------|---------|-------------|
| `now()` | `now()` | Current server timestamp |
| `date(str)` | `date("2024-01-15")` | Date string → timestamp |
| `date(y,m,d,...)` | `date(2024,1,15)` | Components → timestamp |
| `startOfPeriod(p, t)` | `startOfPeriod("monthly", now())` | Round to period start |
| `dateAdd(t, n, unit)` | `dateAdd(now(), -7, "days")` | Add/subtract time |
| `dateDist(t1, t2, p)` | `dateDist(t1, t2, "daily")` | Period count between timestamps |
| `formatTime(fmt, t)` | `formatTime("2006-01", day)` | Timestamp → string |

`dateAdd` units: `"hours"`, `"days"`, `"weeks"`, `"months"`, `"quarters"`, `"years"`.

`dateDist` periods: `"daily"`, `"weekly"`, `"monthly"`, etc.

`formatTime` uses Go reference time format: `2006` = year, `01` = month, `02` = day, `15` = hour, `04` = minute, `05` = second.

#### Utility

| Function | Example | Description |
|----------|---------|-------------|
| `list(a, b, c)` | `list("x","y","z")` | Create a list literal |
| `expandAppIds(pat)` | `expandAppIds("*")` | Expand to matching app IDs |
| `eventSubType(type)` | `eventSubType(type)` | Extract event sub-type string |

### Expression Examples

```
// Numeric comparisons
numEvents > 10
numMinutes >= 0.5

// String matching
contains(visitorId, "@acme.com")
accountId != ""

// Null handling
if(isNull(daysActive), 0, daysActive)
!isNull(parameters.campaign)

// Compound logic
numEvents > 5 && !isNull(accountId)
identified(visitorId) || accountId == "internal"

// Arithmetic in aggregators
{"sum": "numEvents * numMinutes"}
{"avg": "numEvents / if(numMinutes == 0, 1, numMinutes)"}

// Date expressions in timeSeries
"first": "startOfPeriod(\"monthly\", dateAdd(now(), -6, \"months\"))"
"first": "date(2024, 1, 1)"

// Formatting timestamps in eval/select
{"eval": {"dateStr": "formatTime(\"2006-01-02\", day)"}}
```
