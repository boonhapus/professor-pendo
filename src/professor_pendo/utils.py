from typing import Any
import datetime as dt
import logging
import sys

from structlog.types import EventDict, Processor
import structlog


def date_to_ms(date: dt.date | dt.datetime | None) -> int | None:
    """Convert a date or datetime to Pendo-compatible epoch milliseconds."""
    if date is None:
        return None

    if isinstance(date, dt.date):
        date = dt.datetime.combine(date, dt.datetime.min.time())

    return int(date.timestamp() * 1000)


def setup_logging(log_level: int = logging.INFO) -> None:
    """Configures structlog with a standard JSON renderer for CLI scripts."""

    # ── stdlib bridge ────────────────────────────────────────────────────────

    bridge_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(sort_keys=False),
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
        ],
    )

    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(bridge_formatter)

    r = logging.getLogger()
    r.addHandler(h)
    r.setLevel(log_level)

    # ── structlog ────────────────────────────────────────────────────────────

    def rename_keys_for_llm(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        """Renames keys to minimize token usage for LLM ingestion."""
        renames = {
            "timestamp": "ts",
            "level": "lvl",
            "logger": "lgr",
            "event": "msg",
            "func_name": "fn",
            "lineno": "ln",
            "exception": "exc"
        }
        return {renames.get(k, k): v for k, v in event_dict.items()}

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
        structlog.processors.format_exc_info,
        rename_keys_for_llm,
        # This wrapper is what allows the stdlib bridge to see the dict
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )