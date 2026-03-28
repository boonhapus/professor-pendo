# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "cyclopts",
#   "structlog",
# ]
# ///
from dataclasses import asdict, dataclass, field
from typing import Annotated, Any
import json
import logging
import re
import sys

from cyclopts import App, Parameter
import structlog

type ExitCodeT = int
LOGGER = structlog.get_logger(__name__)

# -- CLI ---

app = App(
    name="evaluate-selector",
    help=(
        "Score a CSS selector for resistance to DOM changes (0–100, higher is more stable). "
        "Bonuses: data-test attributes, semantic data-*, ARIA, static IDs, semantic classes, "
        "[name=], stable hrefs. Penalties: depth, hashed classes, positional pseudos, "
        "utility/framework classes, bare tags, :contains(), adjacent combinators."
    ),
)


@app.default
def main(
    selector: Annotated[str, Parameter(help="CSS selector string to evaluate.")],
    *,
    emit_json: Annotated[bool, Parameter("--json", help="Print machine-readable JSON instead of a text report.")] = False,
) -> ExitCodeT:
    trimmed = selector.strip()
    if not trimmed:
        LOGGER.error("selector_empty")
        return 1

    result = calculate_selector_stability(trimmed)

    if emit_json:
        payload: dict[str, Any] = {
            "selector": trimmed,
            "score": result.score,
            "grade": result.grade,
            "grade_emoji": result.grade_emoji,
            "bonuses": result.bonuses,
            "penalties": result.penalties,
            "details": {k: v for k, v in asdict(result.details).items() if v is not None},
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(_format_human(result, trimmed))

    return 0


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class StabilityDetails:
    dataTestAttribute: bool | None = None
    semanticDataAttribute: bool | None = None
    ariaAttribute: bool | None = None
    staticId: bool | None = None
    semanticClass: bool | None = None
    nameAttribute: bool | None = None
    semanticHref: bool | None = None
    deepSelector: bool | None = None
    depth: int | None = None
    depthPenalty: int | None = None
    dynamicClass: bool | None = None
    dynamicClassCount: int | None = None
    positionalSelector: bool | None = None
    positionalCount: int | None = None
    implementationClass: bool | None = None
    bareHtmlElement: bool | None = None
    unqualifiedGenericTag: bool | None = None
    textContentSelector: bool | None = None
    textContentCount: int | None = None
    adjacentCombinator: bool | None = None


@dataclass
class StabilityResult:
    score: int
    grade: str
    grade_emoji: str
    details: StabilityDetails = field(default_factory=StabilityDetails)
    bonuses: list[tuple[str, int]] = field(default_factory=list)
    penalties: list[tuple[str, int]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------


def has_data_test_attribute(selector: str) -> bool:
    return bool(re.search(r"\[data-(test|cy|testid|qa|automation)", selector, re.IGNORECASE))


def has_semantic_data_attribute(selector: str) -> bool:
    has_non_test = bool(re.search(r"\[data-(?!test|cy|testid|qa|automation)[a-z]", selector, re.IGNORECASE))

    standard_attrs_pattern = re.compile(
        r"\[(id|class|style|href|src|alt|title|type|name|value|placeholder|"
        r"disabled|readonly|required|checked|selected|for|action|method|target|"
        r"rel|width|height|size|maxlength|minlength|min|max|step|pattern|accept|"
        r"multiple|autocomplete|autofocus|enctype|novalidate|formaction|formenctype|"
        r"formmethod|formnovalidate|formtarget|download|hreflang|media|ping|"
        r"referrerpolicy|charset|content|http-equiv|lang|dir|tabindex|accesskey|"
        r"contenteditable|draggable|dropzone|hidden|spellcheck|translate|role|aria-[a-z])",
        re.IGNORECASE,
    )

    attr_matches = re.findall(r"\[([a-z][a-z0-9-]*)", selector, re.IGNORECASE)
    for attr_name in attr_matches:
        if not standard_attrs_pattern.match(f"[{attr_name}") and not re.match(r"^data-", attr_name, re.IGNORECASE):
            return True

    return has_non_test


def has_aria_attribute(selector: str) -> bool:
    return bool(re.search(r"\[aria-|role=", selector, re.IGNORECASE))


def has_static_id(selector: str) -> bool:
    hash_match = re.search(r"#([a-zA-Z][\w-]*)", selector)
    if hash_match:
        id_val = hash_match.group(1)
        return not re.match(r"^\d+$", id_val) and not re.search(r"-\d{6,}$", id_val)

    attr_match = re.search(r'\[id[\^*$]?=["\']([^"\']+)["\']\]', selector)
    if attr_match:
        id_val = attr_match.group(1)
        return (
            bool(re.match(r"^[a-zA-Z]", id_val))
            and not re.match(r"^\d+$", id_val)
            and not re.search(r"-\d{6,}$", id_val)
        )

    return False


def has_semantic_class(selector: str) -> bool:
    patterns = [
        r"\.(button|btn|submit|cancel|close|open)",
        r"\.(modal|dialog|dropdown|menu|nav)",
        r"\.(header|footer|sidebar|content|main)",
        r"\.(user|profile|card|item|list)",
        r"\.(form|input|select|checkbox|radio)",
        r"\.(primary|secondary|success|error|warning)",
    ]
    return any(re.search(p, selector, re.IGNORECASE) for p in patterns)


def has_name_attribute(selector: str) -> bool:
    return bool(re.search(r"\[name=", selector, re.IGNORECASE))


def has_semantic_href(selector: str) -> bool:
    href_match = re.search(r'\[href[\^*$]?=["\']([^"\']+)["\']\]', selector)
    if not href_match:
        return False
    href_val = href_match.group(1)
    if href_val.startswith("#"):
        return False
    if re.match(r"^(https?:)?//", href_val):
        return False
    if re.search(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", href_val):
        return False
    if re.search(r"/\d{6,}", href_val):
        return False
    if re.match(r"^/[a-z]", href_val, re.IGNORECASE):
        return True
    if re.match(r"^[a-z][a-z0-9_-]*/", href_val, re.IGNORECASE):
        return True
    return False


def get_selector_depth(selector: str) -> int:
    cleaned = re.sub(r"\[[^\]]+\]", "", selector)
    cleaned = re.sub(r":[a-z-]+\([^)]*\)", ":pseudo", cleaned, flags=re.IGNORECASE)
    combinators = re.findall(r"\s*[>+~]\s*|\s+", cleaned)
    return len(combinators) + 1


def count_positional_selectors(selector: str) -> int:
    matches = re.findall(
        r":nth-[^(\s]*(?:\([^)]*\))?|:first-[^\s>+~]*|:last-[^\s>+~]*|:only-[^\s>+~]*",
        selector,
        re.IGNORECASE,
    )
    return len(matches)


def has_unqualified_generic_tag(selector: str) -> bool:
    components = re.split(r"\s*[>+~]\s*|\s+", selector)
    generic_tags = {"div", "span", "section", "article"}
    for comp in components:
        trimmed = comp.strip().lower()
        if trimmed in generic_tags and not re.search(r"[#.\[:]", comp):
            return True
    return False


def count_dynamic_classes(selector: str) -> int:
    matches = re.findall(r"\.[a-z]+-[a-f0-9]{6,}|\.css-[a-z0-9]+", selector, re.IGNORECASE)
    return len(matches)


def has_implementation_class(selector: str) -> bool:
    patterns = [
        r"\.(col|row|container|grid)-[^\s>+~]*",
        r"\.(flex|block|inline|hidden|visible)-[^\s>+~]*",
        r"\.(m|p|mt|mb|ml|mr|pt|pb)-\d[^\s>+~]*",
        r"\.(text|bg|border|rounded)-[^\s>+~]*",
        r"\.(w|h)-\d[^\s>+~]*|\.w-full|\.h-full",
    ]
    return any(re.search(p, selector, re.IGNORECASE) for p in patterns)


def count_text_content_selectors(selector: str) -> int:
    matches = re.findall(r":contains\([^)]*\)", selector, re.IGNORECASE)
    return len(matches)


def has_adjacent_combinator(selector: str) -> bool:
    return bool(re.search(r"[+~]", selector))


def is_bare_html_element(selector: str) -> bool:
    components = re.split(r"\s*[>+~]\s*|\s+", selector)
    html_elements = {
        "div",
        "section",
        "header",
        "footer",
        "nav",
        "main",
        "article",
        "aside",
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "span",
        "a",
        "img",
        "svg",
        "video",
        "audio",
        "picture",
        "canvas",
        "form",
        "input",
        "button",
        "label",
        "select",
        "textarea",
        "ul",
        "ol",
        "li",
        "figure",
        "figcaption",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
        "dialog",
        "iframe",
    }
    for comp in components:
        trimmed = comp.strip()
        if trimmed.lower() in html_elements and not re.search(r"[#.\[:]", trimmed):
            return True
    return False


# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

GRADES: list[tuple[int, str, str]] = [
    (85, "🟢", "Very Stable"),
    (50, "🔵", "Stable"),
    (25, "🟡", "Fragile"),
    (0, "🔴", "Very Fragile"),
]


def get_grade(score: int) -> tuple[str, str]:
    for threshold, emoji, label in GRADES:
        if score >= threshold:
            return emoji, label
    return "🔴", "Very Fragile"


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def calculate_selector_stability(selector: str) -> StabilityResult:
    if not selector or not isinstance(selector, str):
        return StabilityResult(score=0, grade="Very Fragile", grade_emoji="🔴")

    score = 50
    details = StabilityDetails()
    bonuses: list[tuple[str, int]] = []
    penalties: list[tuple[str, int]] = []

    if has_data_test_attribute(selector):
        details.dataTestAttribute = True
        score += 50
        bonuses.append(("Data test attribute", 50))

    if has_semantic_data_attribute(selector):
        details.semanticDataAttribute = True
        score += 35
        bonuses.append(("Semantic data attribute", 35))

    if has_aria_attribute(selector):
        details.ariaAttribute = True
        score += 25
        bonuses.append(("ARIA attribute", 25))

    if has_static_id(selector):
        details.staticId = True
        score += 25
        bonuses.append(("Static ID", 25))

    if has_semantic_class(selector):
        details.semanticClass = True
        score += 20
        bonuses.append(("Semantic class", 20))

    if has_name_attribute(selector):
        details.nameAttribute = True
        score += 15
        bonuses.append(("Name attribute", 15))

    if has_semantic_href(selector):
        details.semanticHref = True
        score += 15
        bonuses.append(("Semantic href", 15))

    depth = get_selector_depth(selector)
    details.depth = depth
    if depth > 2:
        details.deepSelector = True
        penalty = (depth - 2) * 8
        details.depthPenalty = penalty
        score -= penalty
        penalties.append((f"Deep selector (depth {depth})", penalty))

    dynamic_count = count_dynamic_classes(selector)
    if dynamic_count > 0:
        details.dynamicClass = True
        details.dynamicClassCount = dynamic_count
        penalty = dynamic_count * 35
        score -= penalty
        penalties.append((f"Dynamic class ×{dynamic_count}", penalty))

    positional_count = count_positional_selectors(selector)
    if positional_count > 0:
        details.positionalSelector = True
        details.positionalCount = positional_count
        penalty = positional_count * 30
        score -= penalty
        penalties.append((f"Positional selector ×{positional_count}", penalty))

    if has_implementation_class(selector):
        details.implementationClass = True
        score -= 25
        penalties.append(("Implementation/framework class", 25))

    if is_bare_html_element(selector):
        details.bareHtmlElement = True
        score -= 25
        penalties.append(("Bare HTML element", 25))

    if has_unqualified_generic_tag(selector):
        details.unqualifiedGenericTag = True
        score -= 20
        penalties.append(("Unqualified generic tag", 20))

    text_count = count_text_content_selectors(selector)
    if text_count > 0:
        details.textContentSelector = True
        details.textContentCount = text_count
        penalty = text_count * 15
        score -= penalty
        penalties.append((f"Text content selector ×{text_count}", penalty))

    if has_adjacent_combinator(selector):
        details.adjacentCombinator = True
        score -= 15
        penalties.append(("Adjacent combinator (+ or ~)", 15))

    score = max(0, min(100, score))
    emoji, label = get_grade(score)

    return StabilityResult(
        score=score,
        grade=label,
        grade_emoji=emoji,
        details=details,
        bonuses=bonuses,
        penalties=penalties,
    )


def _format_human(result: StabilityResult, selector: str) -> str:
    lines = [
        f"Selector : {selector}",
        f"Score    : {result.score}/100  {result.grade_emoji} {result.grade}",
        "",
    ]
    if result.bonuses:
        lines.append("Bonuses:")
        for label, pts in result.bonuses:
            lines.append(f"  ✅  +{pts:>3}  {label}")
    if result.penalties:
        lines.append("Penalties:")
        for label, pts in result.penalties:
            lines.append(f"  ❌  -{pts:>3}  {label}")
    if not result.bonuses and not result.penalties:
        lines.append("(no rules matched — baseline score of 50)")
    return "\n".join(lines)


if __name__ == "__main__":
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    raise SystemExit(app())
