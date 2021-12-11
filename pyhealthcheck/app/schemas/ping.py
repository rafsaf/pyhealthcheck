from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class ManyPings(BaseModel):
    hostname_list: List[str] = Field(max_items=100)

    class Config:
        schema_extra = {
            "example": {
                "hostname_list": ["rafsaf.pl", "registry.rafsaf.pl", "google.com"]
            }
        }


class SinglePing(BaseModel):
    hostname: str = Field(max_length=1000)

    class Config:
        schema_extra = {"example": {"hostname": "rafsaf.pl"}}


class SinglePingResponse(BaseModel):
    hostname: str = Field(max_length=1000)
    live: bool
    delay: Optional[float]
    message: str

    class Config:
        schema_extra = {
            "example": {
                "hostname": "rafsaf.pl",
                "live": True,
                "delay": 51.58478599969385,
                "message": "Ping response in 51.58478599969385 ms",
            },
        }


class ManyPingsResponse(BaseModel):
    live: int
    not_live: int
    results: list[SinglePingResponse]

    class Config:
        schema_extra = {
            "example": {
                "live": 2,
                "not_live": 1,
                "results": [
                    {
                        "hostname": "xddd.com",
                        "live": False,
                        "delay": None,
                        "message": "Timed out",
                    },
                    {
                        "hostname": "google.com",
                        "live": True,
                        "delay": 11.942493998503778,
                        "message": "Ping response in 11.942493998503778 ms",
                    },
                    {
                        "hostname": "rafsaf.pl",
                        "live": True,
                        "delay": 166.7080059996806,
                        "message": "Ping response in 166.7080059996806 ms",
                    },
                ],
            },
        }
