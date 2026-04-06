from typing import Annotated, Any, Literal

# ── General Types ─────────────────────────────────────────────────────

type ExitCodeT = Annotated[int, "OS-level exit code"]

# ── Pendo Types ───────────────────────────────────────────────────────

type DataEnvironmentT = Literal["io", "eu", "us1", "jpn", "au"]
"""
The Pendo signifier for the GCP data region.

Further reading:
https://support.pendo.io/hc/en-us/articles/22832528657179-Global-data-hosting
"""

type AggregationPipelineT = list[dict[str, Any]]
"""The shape of one or many pipelines."""
