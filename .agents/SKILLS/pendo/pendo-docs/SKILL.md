---
name: pendo-docs
description: >
  Answer questions about Pendo features, concepts, SDK usage, API integration, and platform
  capabilities by fetching live Pendo documentation and returning a direct source link. Use
  this skill whenever a user asks about how Pendo works, how to configure or install something,
  what a Pendo feature does, how to use the Pendo API or SDK, guide behavior, analytics
  concepts, NPS/surveys, integrations, tagging, or any Pendo-related "how do I" or "what is"
  question that is NOT purely a request for their own subscription data (visitors, accounts,
  guide analytics, etc.). When in doubt, use this skill — it's better to fetch and confirm
  than to answer from stale memory.
metadata:
  version: "0.1.0"
  pendo_mcp: false
  pendo_api: false
---

# Pendo Documentation Skill

Answer Pendo product questions by consulting live documentation and always returning a source link.

## Beta release

This skill is **beta** (`metadata.version`). Treat it as ready to use with these expectations:

- **Live fetch wins.** The `references/` indexes speed up URL lookup; they are periodically regenerated and can drift. Always **fetch the live page** (or Swagger/OpenAPI) for authoritative wording, parameters, and steps.
- **Engage API index.** If OpenAPI at `https://engageapi.pendo.io/swagger.json` cannot be read, `engage-api.md` falls back to a short static summary; agents should still use search or Swagger for full paths and schemas.
- **Maintainers.** Re-run `scripts/refresh_docs.py` from the repo root before a release or on a schedule (see [Keeping references current](#keeping-references-current)).

## When to Use This Skill vs. the Pendo MCP

| Question type | Use |
|---|---|
| "How does X feature work?", "How do I configure Y?", "What is Z?" | **This skill** (docs) |
| "Show me my visitors", "How many guide views did we get?", "Pull our NPS data" | **Pendo MCP** (`https://app.pendo.io/mcp/v0/shttp`) |
| Mixed ("How does NPS work and what's our score?") | **Both** — docs for concept, MCP for data |

---

## Documentation Sources

Always pick the most targeted source. Never guess — fetch and verify.

| Topic area | Primary source | Root URL |
|---|---|---|
| Features, guides, NPS, analytics, installation, integrations, tagging, settings | **Help Center** | `https://support.pendo.io/hc/en-us/` |
| REST API (aggregation, metadata, guides CRUD, events, etc.) | **Engage API** | `https://engageapi.pendo.io/` |
| JavaScript SDK (initialize, config, public functions, events, cookies) | **Web SDK** | `https://web-sdk.pendo.io/` |
| iOS, Android, React Native, Flutter mobile integration | **Mobile SDK (GitHub)** | `https://github.com/pendo-io/pendo-mobile-sdk` |

See the per-source reference files in `references/` for pre-built URL indexes (kept current by `scripts/refresh_docs.py`):

| File | Contents |
|---|---|
| `references/help-center.md` | Full article index from sitemap.xml |
| `references/web-sdk.md` | All Web SDK pages + public function table |
| `references/engage-api.md` | API endpoints + auth reference |
| `references/mobile-sdk.md` | GitHub repo tree by platform |
| `references/doc-map.md` | URL patterns + search query guide (static) |

**Load the relevant reference file before fetching** — search it for the user's keywords first, then fetch only the exact URL that matches.

---

## Workflow

### Step 1 — Classify the question

Determine:
- **Topic**: guides, analytics, NPS/surveys, tagging, installation, API, SDK, mobile, integrations, sessions/replay, feedback
- **Source**: which documentation source above covers this topic
- **Type**: conceptual ("what is") vs. procedural ("how do I") vs. reference ("what are the params for")

### Step 2 — Find the right URL

**First: search the relevant reference file** (loaded from `references/`). Scan for keywords matching the question. If a close match exists, use that URL directly with your environment’s HTTP fetch tool (e.g. `web_fetch` / MCP fetch).

**If no match in the reference file**, fall back to live search:

**For Help Center questions**, use `web_search` since the Help Center blocks direct index fetches:
```
site:support.pendo.io <topic keywords>
```
Pick the most relevant result URL, then `web_fetch` it for full content.

**For Web SDK questions**, the site is fully crawlable. Navigate directly:
- Config options → `https://web-sdk.pendo.io/config/`
- Public functions → `https://web-sdk.pendo.io/public/classic-guides`
- Events → `https://web-sdk.pendo.io/events/browser-events`
- Cookies/storage → `https://web-sdk.pendo.io/cookies/localstorage`
- Advanced → `https://web-sdk.pendo.io/advanced/auto-frame-install`

**For API questions**, fetch the OpenAPI spec or search for the endpoint:
```
site:engageapi.pendo.io <endpoint or resource name>
```

**For Mobile SDK questions**, fetch the README or relevant platform folder:
```
https://github.com/pendo-io/pendo-mobile-sdk/blob/master/README.md
```
Or search:
```
site:github.com/pendo-io/pendo-mobile-sdk <platform> <topic>
```

### Step 3 — Compose the answer

Structure every response like this:

1. **Direct answer** — Answer the question concisely in your own words using the fetched content.
2. **Key details** — Include config options, code snippets, or step-by-step instructions as appropriate.
3. **Source link** — Always end with a clearly labeled documentation link:
   > 📖 **Docs**: [Page title](exact-url)

If multiple pages are relevant, link all of them.

### Step 4 — Flag subscription-specific follow-ups

If the user's question suggests they want to *see their actual data* (not just understand a concept), offer to pull it via the Pendo MCP:
> "Want me to pull your actual [NPS scores / guide data / visitor list] from your Pendo subscription? I can do that too."

---

## Topic Routing Quick Reference

| User says... | Go to |
|---|---|
| "How do I install Pendo?", "snippet", "initialize" | Help Center + Web SDK |
| "Guide isn't showing", "guide targeting", "segment", "activation" | Help Center (search `guides`) |
| "Tooltips", "walkthroughs", "lightboxes", "banners" | Help Center (search guide type) |
| "NPS", "surveys", "poll" | Help Center (search `NPS` or `surveys`) |
| "Page tagging", "feature tagging", "track events" | Help Center (search `tagging`) |
| "Analytics", "funnels", "retention", "paths", "reports" | Help Center (search topic) |
| "pendo.initialize", "excludeAllText", "disableCookies", "config options" | Web SDK → `/config/` |
| "pendo.track()", "pendo.identify()", public API methods | Web SDK → `/public/` |
| "REST API", "aggregation endpoint", "metadata API", "guide CRUD" | Engage API |
| "iOS", "Android", "React Native", "Flutter", "mobile SDK" | Mobile SDK (GitHub) |
| "Salesforce", "Zendesk", "HubSpot", "Slack" integration | Help Center (search `integrations`) |
| "Session Replay", "recording", "Replay" | Help Center + Web SDK `/config/replay` |
| "CSP", "Content Security Policy", "cross-origin" | Web SDK + Help Center |

---

## Keeping references current

The reference files are generated by `scripts/refresh_docs.py`. Run from the **professor-pendo repository root** (after `uv sync`) so the script resolves correctly:

```bash
# Refresh everything
uv run .agents/SKILLS/pendo/pendo-docs/scripts/refresh_docs.py

# Refresh a single source
uv run .agents/SKILLS/pendo/pendo-docs/scripts/refresh_docs.py --source help-center
uv run .agents/SKILLS/pendo/pendo-docs/scripts/refresh_docs.py --source web-sdk
uv run .agents/SKILLS/pendo/pendo-docs/scripts/refresh_docs.py --source engage-api
uv run .agents/SKILLS/pendo/pendo-docs/scripts/refresh_docs.py --source mobile-sdk
```

If you are developing **unpublished** changes to the `professor_pendo` package, use:

```bash
uv run --with-editable . .agents/SKILLS/pendo/pendo-docs/scripts/refresh_docs.py
```

Requires **Python ≥3.14** (see the script’s PEP 723 header). No credentials are required — all sources are public. `references/doc-map.md` is a static file (hand-maintained) and is not overwritten by the script.

---

## Quality Rules

- **Never answer from memory alone** for specific config params, endpoint details, or step-by-step instructions. Always fetch.
- **Always include a doc link** — this is non-negotiable. If you can't reach a page, say so and provide the root URL.
- **Don't conflate subscription data with documentation**. "How many guides do I have?" is a MCP question. "How do guides work?" is a docs question.
- **Prefer specificity**: link to the exact article or section, not just the Help Center homepage.
- If the Help Center search returns no usable results, fall back to a broader `web_search` query like: `pendo.io <topic>` or `pendo help <topic>`.
