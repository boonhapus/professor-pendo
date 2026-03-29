---
name: css-selector-stability
description: >
  Evaluates CSS selectors for stability — how resistant they are to breaking
  when the DOM changes. Returns a score from 0–100 with an explanation of
  what makes the selector strong or fragile. Use this skill whenever a user
  asks about selector quality, whether a selector is "good", wants to compare
  two selectors, needs advice on picking a stable selector for automated
  testing (Cypress, Playwright, Selenium, etc.), or pastes a CSS selector and
  asks for feedback. Also trigger when the user mentions brittle tests, flaky
  selectors, or asks how to improve a locator.
metadata:
  version: "0.1.0"
---

# CSS Selector Stability Evaluator

Score any CSS selector from 0–100. Higher = more resistant to DOM changes.

## When to use

- User shares a selector and asks if it's good / stable / reliable
- User asks which of two selectors is better
- User is writing automated tests and wants selector guidance
- User mentions flaky, brittle, or breaking selectors
- User asks what `data-testid` or `aria-*` selectors are

---

## How to run an evaluation

Use the bundled Python script. No dependencies beyond the standard library.

```bash
uv run scripts/evaluate_selector.py "<selector>"
# or for machine-readable output:
uv run scripts/evaluate_selector.py --json "<selector>"
```

The script is at `scripts/evaluate_selector.py` relative to this SKILL.md.

---

## Scoring overview

**Baseline: 50** — every selector starts here, then bonuses and penalties are applied.

### Bonuses (things that increase stability)

| Rule | Points | What it looks for |
|---|---|---|
| Data test attribute | +50 | `[data-testid=…]`, `[data-cy=…]`, `[data-qa=…]` etc. |
| Semantic data attribute | +35 | Any non-test `data-*` attr, or custom attribute |
| ARIA attribute | +25 | `[aria-label=…]`, `[role=…]` etc. |
| Static ID | +25 | `#myId` or `[id="myId"]` (non-generated) |
| Semantic class | +20 | `.btn`, `.modal`, `.card`, `.error`, etc. |
| Name attribute | +15 | `[name="fieldname"]` on form elements |
| Semantic href | +15 | `[href="/settings"]` — path-based, not hash/UUID |

### Penalties (things that reduce stability)

| Rule | Points | What it looks for |
|---|---|---|
| Deep selector | -8 × extra levels | More than 2 combinator levels |
| Dynamic class | -35 × count | `.css-a1b2c3`, `.sc-hash`, hashed classnames |
| Positional selector | -30 × count | `:nth-child()`, `:first-child`, `:last-of-type`, etc. |
| Implementation class | -25 | Tailwind/Bootstrap utilities: `.flex-1`, `.mt-4`, `.col-6` |
| Bare HTML element | -25 | A selector component that is just a tag: `button`, `div`, `span` |
| Unqualified generic tag | -20 | `div` or `span` alone with no qualifier |
| Text content selector | -15 × count | `:contains("text")` |
| Adjacent combinator | -15 | `+` or `~` combinators |

Final score is clamped to **0–100**.

### Grades

| Score | Grade |
|---|---|
| 85–100 | 🟢 Very Stable |
| 50–84 | 🔵 Stable |
| 25–49 | 🟡 Fragile |
| 0–24 | 🔴 Very Fragile |

---

## Presenting results to the user

> ⚠️ **ALWAYS include the grade color emoji and numeric score when presenting any evaluation result or rule feedback.** This applies to every selector mentioned in the response — including inline comparisons, partial evaluations, and quick answers. Never describe a selector as "stable" or "fragile" in plain text without also showing the corresponding emoji and score (e.g. 🟢 92/100).

After running the script, report:

1. **The score and grade** — lead with this (e.g. `🟢 92/100 Very Stable`)
2. **What's helping** (bonuses) — if any
3. **What's hurting** (penalties) — if any
4. **A one-sentence recommendation** — e.g. "Consider adding a `data-testid` attribute to make this selector purpose-built for testing."

If the user shares multiple selectors, evaluate each and recommend the best one.

---

## Common recommendations to offer

- **Score < 50**: suggest adding `data-testid` or `data-cy` to the element
- **Dynamic classes detected**: explain CSS-in-JS churn and suggest data attributes
- **Positional selectors**: suggest anchoring to an ID or test attribute instead
- **Deep selectors**: suggest flattening or scoping to a stable ancestor
- **Bare HTML elements**: suggest adding a class or attribute qualifier
- **Framework classes**: suggest using semantic or purpose-built class names

---

## Example outputs

```
Selector : [data-testid="submit-btn"]
Score    : 100/100  🟢 Very Stable

Bonuses:
  ✅  +50  Data test attribute
```

```
Selector : div:nth-child(3) > span.css-a1b2c3
Score    : 0/100  🔴 Very Fragile

Penalties:
  ❌  -35  Dynamic class ×1
  ❌  -30  Positional selector ×1
  ❌  -25  Bare HTML element
  ❌  -20  Unqualified generic tag
```