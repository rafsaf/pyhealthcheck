import asyncio
from typing import Any, Coroutine, Optional
import aioping
import _socket
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.schemas.ping import SinglePingResponse
from .. import deps

router = APIRouter(prefix="/ping")


class ErrorResponses:
    time_out = "Timed out"
    invalid_host = "Name or service not known, invalid hostname"
    unknown = "Unknown error"
    to_many_hostnames = "Too many hostnames. Maximum number is 50."


async def make_ping(hostname: str, timeout: int) -> schemas.SinglePingResponse:
    live: bool = False
    delay: Optional[float] = None
    message: str = ""
    for i in range(3000):
        i ** i
    try:
        delay = await aioping.ping(hostname, timeout=timeout) * 1000  # type: ignore
    except TimeoutError:
        message = ErrorResponses.time_out
    except _socket.gaierror:
        message = ErrorResponses.invalid_host
    except Exception:
        message = ErrorResponses.unknown
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
    print(asyncio.get_event_loop_policy())
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
    """
    if len(ping_data.hostname_list) > 50:
        return JSONResponse(
            status_code=400, content={"message": ErrorResponses.to_many_hostnames}
        )
    async_results: list[Coroutine[Any, Any, SinglePingResponse]] = []

    for hostname in ping_data.hostname_list:
        async_results.append(make_ping(hostname, timeout))

    ping_results = await asyncio.gather(*async_results)
    live = 0
    not_live = 0
    single_ping_response: SinglePingResponse
    for single_ping_response in ping_results:
        if single_ping_response.live:
            live += 1
        else:
            not_live += 1

    return {"live": live, "not_live": not_live, "results": ping_results}
