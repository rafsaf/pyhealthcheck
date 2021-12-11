import asyncio
from typing import Any, Coroutine, Optional

import _socket
import aioping
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app import schemas
from app.schemas.ping import SinglePingResponse

router = APIRouter(prefix="/ping")


class PingErrorResponses:
    time_out = "Timed out"
    invalid_host = "Name or service not known, invalid hostname"
    unknown = "Unknown error"
    to_many_hostnames = "Too many hostnames. Maximum number is 50."


async def make_ping(hostname: str, timeout: int) -> schemas.SinglePingResponse:
    live: bool = False
    delay: Optional[float] = None
    message: str = ""
    try:
        delay = await aioping.ping(hostname, timeout=timeout) * 1000  # type: ignore
    except TimeoutError:
        message = PingErrorResponses.time_out
    except _socket.gaierror:
        message = PingErrorResponses.invalid_host
    except Exception:
        message = PingErrorResponses.unknown
    else:
        message = f"Ping response in {delay} ms"
        live = True
    finally:
        return schemas.SinglePingResponse.parse_obj(
            {"hostname": hostname, "live": live, "delay": delay, "message": message}
        )


@router.post(
    "/single",
    status_code=200,
    response_model=schemas.SinglePingResponse,
    responses={400: {"model": schemas.SinglePingResponse}},
)
async def make_single_ping(
    ping_data: schemas.SinglePing,
    timeout: int = Query(default=2, description="Timeout in seconds for every ping"),
):
    """
    Make ICMP ping to single hostname or IP address.
    """
    result = await make_ping(ping_data.hostname, timeout)
    if result.live:
        return result
    else:
        return JSONResponse(status_code=400, content=result.dict())


@router.post(
    "/many",
    status_code=200,
    response_model=schemas.ManyPingsResponse,
    responses={400: {"model": schemas.ErrorMessage}},
)
async def make_many_pings(
    ping_data: schemas.ManyPings,
    timeout: int = Query(default=2, description="Timeout in seconds for every ping"),
):
    """
    Make ICMP pings to up to 50 hostnames or IP addresses.
    Warning, `results` list is returned not necessarily in the order of `hostname_list`. Duplicated hostnames are ommited.
    """
    if len(ping_data.hostname_list) > 50:
        return JSONResponse(
            status_code=400, content={"message": PingErrorResponses.to_many_hostnames}
        )
    async_results: list[Coroutine[Any, Any, SinglePingResponse]] = []

    for hostname in ping_data.hostname_list:
        async_results.append(make_ping(hostname, timeout))

    ping_results = await asyncio.gather(*async_results)

    live = sum((result.live for result in ping_results))
    not_live = len(ping_results) - live

    return {"live": live, "not_live": not_live, "results": ping_results}
