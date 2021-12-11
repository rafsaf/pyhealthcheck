from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class HealthStack(BaseModel):
    custom_name: Optional[str] = Field(max_length=254, min_length=3)
    domains: list[str] = Field(min_items=1)
    delay_between_checks: int = Field(ge=2, le=3600)
    emails_to_alert: list[EmailStr]

    class Config:
        schema_extra = {
            "example": {
                "custom_name": "Fantastic Stack",
                "domains": ["rafsaf.pl", "registry.rafsaf.pl", "google.com"],
                "delay_between_checks": 10,
                "emails_to_alert": ["example@example.com"],
            }
        }
        orm_mode = True


class HealthStackCreate(HealthStack):
    pass
