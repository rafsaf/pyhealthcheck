from typing import List, Optional
from pydantic import BaseModel, validator
from pydantic.networks import EmailStr


class HealthStack(BaseModel):
    custom_name: Optional[str]
    domains: List[str]
    delay_between_checks_seconds: int = 10
    emails_to_alert: List[EmailStr]

    @validator("delay_between_checks_seconds")
    def check_delay_is_reasonable(cls, delay_between_checks_seconds: int):
        if not 2 > delay_between_checks_seconds > 60:
            raise ValueError("delay_between_checks_seconds must be between 2 and 60 ")


class HealthStackCreate(HealthStack):
    pass
