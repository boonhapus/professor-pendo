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
import datetime as dt
import json
import pathlib

from professor_pendo import api, types, utils
from cyclopts import App, Parameter
import dotenv
import niquests
import structlog

LOGGER = structlog.get_logger(__name__)

app = App(
    name="fetch-pendo-features",
    help="Export Pendo features (metadata + rules) via the Aggregation API.",
)


@app.default
async def main(
    *,
    subscription_id: Annotated[int, Parameter(env_var="PENDO_SUBSCRIPTION_ID")],
    integration_key: Annotated[str, Parameter(env_var="PENDO_INTEGRATION_KEY")],
    data_environment: Annotated[types.DataEnvironmentT, Parameter(env_var="PENDO_DATA_ENVIRONMENT")] = "io",
    output: pathlib.Path = pathlib.Path(".data/tmp/pendo_features.json"),
    # ── Aggregation Filters ───────────────────────────────────────────
    app_id: Annotated[int, Parameter(help='ID found in.. Subcription Settings > App > in the URL')] = -323232,
    updated_since: Annotated[dt.date | None, Parameter(help="Compared against feature.lastUpdatedAt")] = None,
    created_since: Annotated[dt.date | None, Parameter(help="Compared against feature.createdAt")] = None,
    author: Annotated[str | None, Parameter(help="Compared against createdByUser.id")] = None,
    product_area: Annotated[str | None, Parameter(help='Name of the Product Area to filter by')] = None,
) -> types.ExitCodeT:

    # ── PREPARE ───────────────────────────────────────────────────────

    pipeline: types.AggregationPipelineT = [
        {"source": {"features": {"appId": app_id}}},
        {"select": {
            "id": "id",
            "displayName": "name",
            "rules": "elementPathRules",
            "lastUpdatedAt": "lastUpdatedAt",
            "createdAt": "createdAt",
            "author": "createdByUser.username",
            "productArea": "group.name",
        }},
    ]

    if updated_since is not None:
        pipeline.append({"filter": f"lastUpdatedAt >= {utils.date_to_ms(updated_since)}"})

    if created_since is not None:
        pipeline.append({"filter": f"createdAt >= {utils.date_to_ms(created_since)}"})
    
    if author is not None:
        pipeline.append({"filter": f"author == \"{author}\""})

    if product_area is not None:
        pipeline.append({"filter": f"productArea == \"{product_area}\""})

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
