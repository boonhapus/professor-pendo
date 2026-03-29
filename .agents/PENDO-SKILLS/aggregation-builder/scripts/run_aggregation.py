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
import logging
import pathlib
import sys

from professor_pendo import api, types
from cyclopts import App, Parameter
import dotenv
import niquests
import structlog

type ExitCodeT = int
LOGGER = structlog.get_logger(__name__)

# LOAD FROM python-dotenv, SO cyclopts CAN USE THEM AS DEFAULTS
dotenv.load_dotenv()

# -- CLI ---

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
    output: pathlib.Path = pathlib.Path(".data/tmp/pendo_features.json"),
    pipeline: Annotated[pathlib.Path | str, Parameter(help="JSON string of the aggregation pipeline OR a path to a JSON file containing it.")],
) -> ExitCodeT:
    # LOAD THE PIPELINE
    if isinstance(pipeline, pathlib.Path):
        pipeline = pipeline.read_text(encoding="utf-8")

    pipeline = json.loads(pipeline)

    opts = {
        "subscription_id": subscription_id,
        "integration_key": integration_key,
        "data_environment": data_environment,
    }

    try:
        # FETCH DATA
        async with api.PendoAPI(**opts) as client:
            r = await client.aggregation(pipeline=pipeline)
            r.raise_for_status()
            d = r.json()

        # OUTPUT RESULTS
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", encoding="utf-8") as j:
            json.dump(d, j, indent=2, ensure_ascii=False)

        return 0

    except niquests.HTTPError:
        await LOGGER.aerror("aggregation_request_failed", exc_info=True)
        return 1

    except json.JSONDecodeError:
        await LOGGER.aerror("aggregation_invalid_json", exc_info=True)
        return 1    


if __name__ == "__main__":
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(), 
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    raise SystemExit(app())
