# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "cyclopts",
#   "niquests",
#   "professor-pendo @ git+https://github.com/boonhapus/professor-pendo",
#   "python-dotenv",
#   "structlog",
# ]
# ///
from typing import Annotated
import json
import pathlib

from professor_pendo import api, types, utils
from cyclopts import App, Parameter
import dotenv
import niquests
import structlog

LOGGER = structlog.get_logger(__name__)

app = App(
    name="run-pendo-aggregation",
    help="Execute arbitrary Pendo aggregation pipelines.",
)


@app.default
async def main(
    *,
    subscription_id: Annotated[int, Parameter(env_var="PENDO_SUBSCRIPTION_ID")],
    integration_key: Annotated[str, Parameter(env_var="PENDO_INTEGRATION_KEY")],
    data_environment: Annotated[types.DataEnvironmentT, Parameter(env_var="PENDO_DATA_ENVIRONMENT")] = "io",
    output: pathlib.Path = pathlib.Path(".data/tmp/aggregation.json"),
    # ── Aggregation Pipeline ──────────────────────────────────────────
    pipeline: Annotated[str, Parameter(help="JSON of the aggregation pipeline (raw string or filepath.json)")],
) -> types.ExitCodeT:

    # ── PREPARE ───────────────────────────────────────────────────────

    try:
        if (fp := pathlib.Path(pipeline)).exists():
            pipeline = fp.read_text()

        pipeline = json.loads(pipeline)
    except json.JSONDecodeError as e:
        await LOGGER.aerror("load_pipeline_failed", error=str(e))
        return 1

    # ── MAIN ──────────────────────────────────────────────────────────

    try:

        # ── FETCH DATA ────────────────────────────────────────────────

        opts = {
            "subscription_id": subscription_id,
            "integration_key": integration_key,
            "data_environment": data_environment,
        }

        async with api.PendoAPI(**opts) as client:
            r = await client.aggregation(pipeline=pipeline)
            r.raise_for_status()
            d = r.json()

        # ── WRITE TO FILE ─────────────────────────────────────────────

        output.parent.mkdir(parents=True, exist_ok=True)

        with output.with_suffix(".json").open("w", encoding="utf-8") as j:
            json.dump(d, j, indent=2, ensure_ascii=False)

        return 0

    except niquests.HTTPError:
        await LOGGER.aerror("aggregation_request_failed", exc_info=True)
        return 1

    except json.JSONDecodeError:
        await LOGGER.aerror("aggregation_invalid_json", exc_info=True)
        return 1    


if __name__ == "__main__":
    utils.setup_logging()
    dotenv.load_dotenv()

    raise SystemExit(app())
