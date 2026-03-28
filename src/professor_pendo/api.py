from typing import Any

import niquests
import structlog

from professor_pendo import types

LOGGER = structlog.get_logger(__name__)


class LoggingHook(niquests.AsyncLifeCycleHook):
    """Structured logging hook for the Pendo API client."""
 
    async def pre_request(self, prepared_request: niquests.PreparedRequest, **kwargs) -> None:
        """
        The prepared request just got built. You may alter it prior to be sent through HTTP.
        
        Further reading:
          https://niquests.readthedocs.io/en/latest/user/advanced.html#niquests.hooks.AsyncLifeCycleHook.pre_request
        """
        await LOGGER.adebug(
            "pendo.request",
            method=prepared_request.method,
            url=str(prepared_request.url),
            body=prepared_request.body,
        )
 
    async def response(self, response: niquests.Response, **kwargs) -> None:
        """
        The response generated from a Request. You may alter the response at will.
        
        Further reading:
          https://niquests.readthedocs.io/en/latest/user/advanced.html#niquests.hooks.AsyncLifeCycleHook.response
        """
        if response.request is None:
            return

        await LOGGER.ainfo(
            "pendo.response",
            method=response.request.method,
            url=str(response.request.url),
            status_code=response.status_code,
            elapsed_s=round(response.elapsed.total_seconds(), 2),
        )


class PendoAPI(niquests.AsyncSession):
    """
    Async HTTP client for the Pendo Engage REST API.

    Usage:
    >>> pendo_api = PendoClient()
    >>> 
    >>> async with pendo_api as client:
    >>>     p = [{"source": {"visitors": None}}]
    >>>     r = await client.aggregate(pipeline=p)
    >>>     r.raise_for_status()
    >>>
    >>>     d = r.json()
    >>>

    Further reading:
      https://engageapi.pendo.io/
    """

    def __init__(
        self,
        *,
        subscription_id: int,
        integration_key: str,
        data_environment: types.DataEnvironmentT = "io",
        **session_opts,
    ) -> None:
        self._sub_id = subscription_id
        self._api_key = integration_key

        super().__init__(
            base_url=f"https://{self.domain_data_evironment(env=data_environment)}/api/v1",
            hooks=LoggingHook(),
            **session_opts,
        )

        # Add the API key and force content-type to JSON only.
        self.headers.update(
            {
                "x-pendo-integration-key": integration_key,
                "content-type": "application/json",
                "accept": "application/json",
            }
        )
    
    @staticmethod
    def domain_data_evironment(env: types.DataEnvironmentT) -> str:
        """Lookup for the data environment."""
        base_url_map = {
            "io": "app.pendo.io",
            "eu": "app.eu.pendo.io",
            "us1": "us1.app.pendo.io",
            "jpn": "app.jpn.pendo.io",
            "au": "app.au.pendo.io",
        }
        return base_url_map.get(env, "app.pendo.io")

    async def aggregation(self, *, pipeline: list[Any]) -> niquests.Response:
        """
        Aggregations are the language for accessing and processing Pendo data.

        They take sources of Pendo data and apply operators to do computations.
        These aggregations are extremely powerful and are used to compute
        almost all analytics found in the Pendo UI.

        Further reading:
          https://engageapi.pendo.io/#7c8479b8-3843-403c-94a9-04cbdf542db9
        """
        b = {"response": {"mimeType": "application/json"}, "request": {"pipeline": pipeline}}
        r = await self.post("/aggregation", json=b)
        return r
