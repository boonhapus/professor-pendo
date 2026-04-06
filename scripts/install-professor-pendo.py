# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "cyclopts",
#   "niquests",
#   "structlog",
# ]
# ///
"""
Copy the `pendo` skills bundle into the folder your editor or CLI expects.

By default the bundle is taken from your **clone** of this repo when `.agents/SKILLS/pendo`
is present; otherwise it is **downloaded** from GitHub (`main` branch ZIP). See `--source` to override.

This matches the **Getting Started** section in the project README.
"""

from __future__ import annotations

import logging
import pathlib
import shutil
import sys
import tempfile
import zipfile
from enum import StrEnum
from typing import Annotated, Literal

import niquests
import structlog
from cyclopts import App, Parameter
from cyclopts.help import DefaultFormatter
from cyclopts.help.specs import PanelSpec, TableSpec
from rich.console import Console

type ExitCodeT = int

# cyclopts + Rich: pin width so --help panels use the full line (not ~80 cols from auto-detect).
CLI_HELP_WIDTH = 105

# Same archive as in README.md (Getting Started).
GITHUB_MAIN_ZIP = (
    "https://github.com/boonhapus/professor-pendo/archive/refs/heads/main.zip"
)

LOGGER = structlog.get_logger(__name__)


class Which(StrEnum):
    """Cursor, Claude Code, or Gemini CLI."""

    cursor = "cursor"
    claude = "claude"
    gemini = "gemini"


app = App(
    name="install-professor-pendo",
    help=(
        "Copy the Pendo skills bundle into the folder Cursor, Claude Code, or Gemini CLI looks for. "
        "Run inside a clone to use the repo copy of the bundle; otherwise the script downloads from GitHub."
    ),
    help_flags=["--help"],
    # Rich only honors explicit width when height is also set; otherwise size falls back to ~80 cols.
    console=Console(width=CLI_HELP_WIDTH, height=24, force_terminal=True),
    help_formatter=DefaultFormatter.with_newline_metadata(
        panel_spec=PanelSpec(width=CLI_HELP_WIDTH),
        # expand=True fills the panel; a fixed table width was squeezing the description column.
        table_spec=TableSpec(expand=True),
    ),
)


def _configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(colors=False),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent


def _cloned_bundle() -> pathlib.Path:
    return _repo_root() / ".agents" / "SKILLS" / "pendo"


def _has_cloned_bundle() -> bool:
    p = _cloned_bundle()
    return p.is_dir() and (p / "SKILL.md").is_file()


def _find_pendo_in_extract_root(extract_root: pathlib.Path) -> pathlib.Path | None:
    """GitHub ZIP contains a single top-level folder (e.g. professor-pendo-main)."""
    for child in extract_root.iterdir():
        if not child.is_dir():
            continue
        candidate = child / ".agents" / "SKILLS" / "pendo"
        if candidate.is_dir() and (candidate / "SKILL.md").is_file():
            return candidate
    return None


def _download_pendo_from_github(work_dir: pathlib.Path) -> pathlib.Path:
    """Download the main-branch ZIP, extract under work_dir, return path to `pendo` bundle."""
    zip_path = work_dir / "_repo.zip"
    try:
        resp = niquests.get(
            GITHUB_MAIN_ZIP,
            headers={"User-Agent": "professor-pendo-install-script"},
            timeout=120,
        )
        resp.raise_for_status()
    except niquests.HTTPError as e:
        code = e.response.status_code if e.response is not None else "?"
        raise RuntimeError(f"Download failed (HTTP {code}): {GITHUB_MAIN_ZIP}") from e
    except niquests.RequestException as e:
        raise RuntimeError(f"Download failed (network): {e}") from e

    zip_path.write_bytes(resp.content)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(work_dir)
    zip_path.unlink(missing_ok=True)

    found = _find_pendo_in_extract_root(work_dir)
    if found is None:
        raise RuntimeError(
            "Could not find `.agents/SKILLS/pendo` inside the downloaded archive."
        )
    return found


def _destination(
    which: Which,
    directory: pathlib.Path,
) -> pathlib.Path:
    if which == Which.claude:
        return pathlib.Path.home() / ".claude" / "skills" / "pendo"
    if which == Which.cursor:
        return directory / ".agents" / "skills" / "pendo"
    return directory / ".gemini" / "skills" / "pendo"


def _copy_tree(src: pathlib.Path, dst: pathlib.Path, *, replace: bool) -> None:
    if dst.exists():
        if not replace:
            raise FileExistsError(dst)
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _effective_source_mode(
    source: Literal["auto", "cloned", "github"],
) -> Literal["cloned", "github"]:
    if source == "cloned":
        return "cloned"
    if source == "github":
        return "github"
    return "cloned" if _has_cloned_bundle() else "github"


@app.default
def main(
    *,
    which: Annotated[
        Which,
        Parameter(
            "--which",
            help="cursor, claude (Claude Code), or gemini (Gemini CLI).",
        ),
    ],
    source: Annotated[
        Literal["auto", "cloned", "github"],
        Parameter(
            help=(
                "auto: use this repo's bundle if present, else download from GitHub. "
                "cloned: only use `.agents/SKILLS/pendo` from this clone (fail if missing). "
                "github: always download from `main` on GitHub."
            ),
        ),
    ] = "auto",
    directory: Annotated[
        pathlib.Path,
        Parameter(
            "--directory",
            help="Project folder for Cursor / Gemini (where `.agents` or `.gemini` should live).",
            show_default=False,
        ),
    ] = pathlib.Path.cwd(),
    replace: Annotated[
        bool,
        Parameter(
            "--replace",
            help="Overwrite the destination folder if it already exists.",
            negative_bool=(),
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        Parameter(
            "--dry-run",
            help="Print what would happen without copying or downloading.",
            negative_bool=(),
        ),
    ] = False,
) -> ExitCodeT:
    mode = _effective_source_mode(source)

    if mode == "cloned" and not _has_cloned_bundle():
        LOGGER.error(
            "missing_cloned_bundle",
            path=str(_cloned_bundle()),
            hint="Clone or unzip the full repo, or use --source github.",
        )
        return 1

    dst = _destination(which, directory.resolve())

    LOGGER.info("install_start")

    if mode == "cloned":
        src = _cloned_bundle()
        LOGGER.info("source", kind="cloned", path=str(src))
    else:
        LOGGER.info("source", kind="github", url=GITHUB_MAIN_ZIP)
        if dry_run:
            LOGGER.info("dry_run_skip", to=str(dst))
            return 0
        try:
            with tempfile.TemporaryDirectory(prefix="professor-pendo-install-") as tmp:
                src = _download_pendo_from_github(pathlib.Path(tmp))
                LOGGER.info("extracted", path=str(src))
                LOGGER.info("destination", path=str(dst))
                _copy_tree(src, dst, replace=replace)
        except FileExistsError:
            LOGGER.error(
                "destination_exists",
                path=str(dst),
                hint="Use --replace or remove the folder by hand.",
            )
            return 1
        except (OSError, RuntimeError) as e:
            LOGGER.error("install_failed", error=str(e))
            return 1
        LOGGER.info(
            "install_done",
            tip="Restart your app or reload the window if new skills do not show up yet.",
        )
        return 0

    LOGGER.info("destination", path=str(dst))

    if dry_run:
        LOGGER.info("dry_run_skip")
        return 0

    try:
        _copy_tree(src, dst, replace=replace)
    except FileExistsError:
        LOGGER.error(
            "destination_exists",
            path=str(dst),
            hint="Use --replace or remove the folder by hand.",
        )
        return 1
    except OSError as e:
        LOGGER.error("copy_failed", error=str(e))
        return 1

    LOGGER.info(
        "install_done",
        tip="Restart your app or reload the window if new skills do not show up yet.",
    )
    return 0


if __name__ == "__main__":
    _configure_logging()
    raise SystemExit(app())
