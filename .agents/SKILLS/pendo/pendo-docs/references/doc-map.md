# Pendo Documentation URL Map

A reference for known deep-link patterns within each documentation source.
Use these to construct targeted fetch URLs rather than starting from scratch.

---

## Help Center — `https://support.pendo.io/hc/en-us/`

The Help Center blocks direct crawling. Always use `web_search` with `site:support.pendo.io` first, then `web_fetch` the result URL.

**Known article patterns:**
```
https://support.pendo.io/hc/en-us/articles/<article-id>-<slug>
https://support.pendo.io/hc/en-us/categories/<category-id>-<slug>
https://support.pendo.io/hc/en-us/sections/<section-id>-<slug>
```

**High-value search queries by topic:**
| Topic | Search query |
|---|---|
| Installation | `site:support.pendo.io install snippet initialize` |
| Guides (general) | `site:support.pendo.io guides in-app` |
| Guide targeting | `site:support.pendo.io guide activation segment targeting` |
| Guide types | `site:support.pendo.io tooltip lightbox walkthrough banner` |
| NPS | `site:support.pendo.io NPS survey` |
| Page tagging | `site:support.pendo.io page tagging` |
| Feature tagging | `site:support.pendo.io feature tagging` |
| Track events | `site:support.pendo.io track events custom` |
| Visitor metadata | `site:support.pendo.io visitor metadata` |
| Analytics/reports | `site:support.pendo.io analytics reports funnels` |
| Integrations | `site:support.pendo.io integrations` |
| Session Replay | `site:support.pendo.io session replay recording` |
| Segments | `site:support.pendo.io segments` |
| Resource Center | `site:support.pendo.io resource center` |
| CSP | `site:support.pendo.io content security policy CSP` |
| Debugging | `site:support.pendo.io debugger troubleshoot agent` |
| Sub/multi-app | `site:support.pendo.io multi-app subscription` |
| Pendo AI | `site:support.pendo.io AI Pendo AI` |

---

## Web SDK — `https://web-sdk.pendo.io/`

Fully crawlable. Fetch pages directly with your environment’s HTTP fetch tool (e.g. `web_fetch`).

```
https://web-sdk.pendo.io/                          # Overview, installation, builds
https://web-sdk.pendo.io/config/                   # All config options index
https://web-sdk.pendo.io/config/analytics          # Analytics config
https://web-sdk.pendo.io/config/core               # Core config (apiKey, visitor, account)
https://web-sdk.pendo.io/config/guides             # Guide config (delay, timeout, globalScripts)
https://web-sdk.pendo.io/config/network-logs       # Network log capture config
https://web-sdk.pendo.io/config/replay             # Session replay config
https://web-sdk.pendo.io/events/browser-events     # Browser events emitted by SDK
https://web-sdk.pendo.io/public/classic-guides     # Public functions index
https://web-sdk.pendo.io/cookies/localstorage      # Cookie and localStorage usage
https://web-sdk.pendo.io/advanced/auto-frame-install  # Advanced: iframes, auto-install
https://web-sdk.pendo.io/releases                  # Release history (beta + stable)
https://web-sdk.pendo.io/versions                  # Version notes
```

**Key public functions** (documented under `/public/`):
- `pendo.initialize()` — core setup
- `pendo.identify()` — update visitor/account
- `pendo.track()` — custom track events
- `pendo.showGuideById()` — programmatic guide activation
- `pendo.stopGuides()` — disable guide display
- `pendo.enableDebugging()` — debug mode

---

## Engage API — `https://engageapi.pendo.io/`

OpenAPI/Swagger-based reference. The root renders a Swagger UI — best to search for specific resources.

**Search query pattern:**
```
site:engageapi.pendo.io <resource>
```

**Known resource areas:**
- Aggregation (analytics queries)
- Guide CRUD
- Feature / Page metadata
- Visitor / Account metadata
- Events (track events, page events, feature events)
- NPS
- Reports

**Direct fetch tip:** The spec may be available at:
```
https://engageapi.pendo.io/swagger.json
```
or linked from the Swagger UI root.

---

## Mobile SDK — `https://github.com/pendo-io/pendo-mobile-sdk`

GitHub repo. README is the entry point; platform-specific guides live in subdirectories.

```
https://github.com/pendo-io/pendo-mobile-sdk/blob/master/README.md
```

**Platform subdirectories** (check repo for current structure):
```
/iOS/         — Native iOS (Swift/Obj-C)
/Android/     — Native Android (Kotlin/Java)
/ReactNative/ — React Native integration
/Flutter/     — Flutter integration
/Xamarin/     — Xamarin integration
```

**Search query pattern:**
```
site:github.com/pendo-io/pendo-mobile-sdk <platform> <topic>
```
Example: `site:github.com/pendo-io/pendo-mobile-sdk Flutter initialize`
