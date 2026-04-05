# Aggregation Examples

Each example shows a natural-language question followed by the complete runnable query. Use these as templates — swap sources, fields, filters, and time ranges to fit the user's request.

---

## 1. List Visitors

**"Give me a list of all identified visitors."**

```json
{
  "response": { "mimeType": "application/json" },
  "request": {
    "requestId": "visitor-list",
    "pipeline": [
      { "source": { "visitors": null } },
      { "identified": "visitorId" },
      { "select": {
          "visitorId": "visitorId",
          "lastVisit": "metadata.auto.lastvisit"
      } },
      { "sort": ["-lastVisit"] },
      { "limit": 100 }
    ]
  }
}
```

---

## 2. Top-N Visitors by Days Active

**"Show me the top 10 most active visitors in the last 30 days."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "top-active-visitors",
    "pipeline": [
      { "source": {
          "events": { "appId": <YOUR_APP_ID>, "blacklist": "apply" },
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -30 }
      } },
      { "identified": "visitorId" },
      { "group": {
          "group": ["visitorId"],
          "fields": [{ "daysActive": { "count": "day" } }]
      } },
      { "sort": ["-daysActive", "visitorId"] },
      { "select": {
          "visitorId": "visitorId",
          "daysActive": "if(isNull(daysActive), 0, daysActive)"
      } },
      { "limit": 10 }
    ]
  }
}
```

**Pipeline logic:** Load 30 days of events → drop anonymous → group per visitor, count unique days → sort descending → top 10.

---

## 3. Total Unique Visitors (Single Metric)

**"How many unique visitors used the app in the last 7 days?"**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "unique-visitors-count",
    "pipeline": [
      { "source": {
          "events": null,
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -7 }
      } },
      { "identified": "visitorId" },
      { "reduce": { "uniqueVisitors": { "count": "visitorId" } } }
    ]
  }
}
```

---

## 4. Daily Visitor Trend (Iterative)

**"Show me unique visitors per day for the last 14 days."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "daily-visitor-trend",
    "pipeline": [
      { "source": {
          "events": null,
          "timeSeries": { "period": "daily", "first": "now()", "count": -14 }
      } },
      { "identified": "visitorId" },
      { "reduce": { "uniqueVisitors": { "count": "visitorId" } } }
    ]
  }
}
```

**Key difference from Example 3:** Period is `daily` (iterative) instead of `dayRange` (aggregate), so the pipeline runs independently per day → 14 result sets.

---

## 5. Breakdown by Visitor Metadata

**"How many events per language group over the last 30 days?"**

```json
{
  "response": { "mimeType": "application/json" },
  "request": {
    "requestId": "events-by-language",
    "pipeline": [
      { "source": {
          "pageEvents": null,
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -30 }
      } },
      { "identified": "visitorId" },
      { "group": {
          "group": ["visitorId"],
          "fields": { "numEvents": { "sum": "numEvents" } }
      } },
      { "bulkExpand": { "visitorMetadata": { "visitor": "visitorId" } } },
      { "group": {
          "group": ["visitorMetadata.agent.language"],
          "fields": [
            { "visitorCount": { "count": null } },
            { "numEvents": { "sum": "numEvents" } }
          ]
      } },
      { "select": {
          "Language": "visitorMetadata.agent.language",
          "Visitor Count": "visitorCount",
          "Event Count": "numEvents"
      } },
      { "sort": ["-Event Count"] }
    ]
  }
}
```

**Pipeline logic:** Load events → deduplicate per visitor → enrich with metadata → re-group by metadata field → present.

---

## 6. OS/Browser Breakdown

**"Count visitors by operating system in the last 30 days."**

```json
{
  "response": { "mimeType": "application/json" },
  "request": {
    "requestId": "os-breakdown",
    "pipeline": [
      { "source": {
          "events": null,
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -30 }
      } },
      { "identified": "visitorId" },
      { "group": { "group": ["visitorId", "userAgent"] } },
      { "useragent": { "userAgent": "userAgent" } },
      { "group": {
          "group": ["userAgent.os"],
          "fields": [{ "count": { "count": null } }]
      } },
      { "select": { "os": "userAgent.os", "count": "count" } },
      { "sort": ["-count"] }
    ]
  }
}
```

---

## 7. Track Event Visitors

**"Get all visitor IDs who triggered track event X yesterday."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "track-event-visitors",
    "pipeline": [
      { "source": {
          "trackEvents": { "appId": "expandAppIds(\"*\")" },
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -1 }
      } },
      { "identified": "visitorId" },
      { "filter": "trackTypeId == \"<YOUR_TRACK_TYPE_ID>\"" },
      { "group": { "group": ["visitorId"] } },
      { "select": { "visitorId": "visitorId" } }
    ]
  }
}
```

---

## 8. Page Parameter Analysis

**"Show me the top 100 URL parameters for a specific page, with event counts."**

```json
{
  "response": { "location": "request", "mimeType": "text/csv" },
  "request": {
    "requestId": "top-page-params",
    "pipeline": [
      { "source": {
          "pageEvents": { "pageId": "<YOUR_PAGE_ID>", "blacklist": "apply" },
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -30 }
      } },
      { "identified": "visitorId" },
      { "filter": "!isNull(parameters.parameter) && parameters.parameter != \"\"" },
      { "group": {
          "group": ["pageId", "parameters.parameter"],
          "fields": [{ "numEvents": { "sum": "numEvents" } }]
      } },
      { "sort": ["-numEvents"] },
      { "limit": 100 }
    ]
  }
}
```

---

## 9. Fork + Join (Multi-Metric per Entity)

**"For each visitor, show both first visit and last visit dates."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "visitor-first-last",
    "pipeline": [
      { "source": { "visitors": null } },
      { "identified": "visitorId" },
      { "fork": [
          [{ "group": {
              "group": ["visitorId"],
              "fields": [{ "firstVisit": { "max": "metadata.auto.firstvisit" } }]
          } }],
          [{ "group": {
              "group": ["visitorId"],
              "fields": [{ "lastVisit": { "min": "metadata.auto.lastvisit" } }]
          } }]
      ] },
      { "join": { "fields": ["visitorId"], "width": 2 } },
      { "sort": ["-lastVisit"] },
      { "limit": 20 }
    ]
  }
}
```

---

## 10. Segment-Filtered Query

**"Count events for visitors in segment X over the last 7 days."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "segment-events",
    "pipeline": [
      { "source": {
          "events": { "appId": <YOUR_APP_ID>, "blacklist": "apply" },
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -7 }
      } },
      { "segment": { "id": "<YOUR_SEGMENT_ID>" } },
      { "identified": "visitorId" },
      { "reduce": {
          "totalEvents": { "sum": "numEvents" },
          "uniqueVisitors": { "count": "visitorId" }
      } }
    ]
  }
}
```

---

## 11. Retention Cohort

**"Show monthly new-user retention for the last 6 months."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "retention-monthly",
    "pipeline": [
      { "source": {
          "timespan": { "kind": "visitor", "appId": "expandAppIds(\"*\")" }
      } },
      { "identified": "visitorId" },
      { "group": {
          "group": ["visitorId"],
          "fields": {
            "activeDays": { "daysActiveUnion": "activeDays" },
            "firstTime": { "min": "firstTime" },
            "lastTime": { "max": "lastTime" }
          }
      } },
      { "retention": {
          "timeSeries": { "period": "monthRange", "first": "date(2024,7,1)", "count": 6 },
          "offset": 30,
          "cohortField": "cohort",
          "relativePeriodsField": "relativePeriod",
          "cohortMode": "first"
      } }
    ]
  }
}
```

---

## 12. Multi-App Events with Enrichment

**"List the last 50 page events across all apps, with visitor email."**

```json
{
  "response": { "location": "request", "mimeType": "application/json" },
  "request": {
    "requestId": "recent-events-enriched",
    "pipeline": [
      { "source": {
          "events": { "appId": "expandAppIds(\"*\")" },
          "timeSeries": { "period": "dayRange", "first": "now()", "count": -1 }
      } },
      { "identified": "visitorId" },
      { "sort": ["-day", "-numEvents"] },
      { "limit": 50 },
      { "bulkExpand": { "v": { "visitor": "visitorId" } } },
      { "select": {
          "visitorId": "visitorId",
          "email": "v.agent.email",
          "page": "pageId",
          "events": "numEvents",
          "day": "day"
      } }
    ]
  }
}
```

**Key pattern:** Limit *before* bulkExpand to avoid expanding every visitor row.

---

## Template: Blank Starting Point

Copy this and fill in the pipeline:

```json
{
  "response": {
    "location": "request",
    "mimeType": "application/json"
  },
  "request": {
    "requestId": "<name>",
    "pipeline": [
      { "source": {
          "<source>": { },
          "timeSeries": {
            "period": "<period>",
            "first": "now()",
            "count": <negative-int>
          }
      } }
    ]
  }
}
```
