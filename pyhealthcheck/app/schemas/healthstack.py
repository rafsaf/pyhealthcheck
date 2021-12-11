from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .user import User


class HealthStack(BaseModel):
    id: int
    custom_name: Optional[str] = Field(max_length=254, min_length=3)
    domains: list[str] = Field(min_items=1)
    delay_between_checks: int = Field(ge=2, le=3600)
    emails_to_alert: list[EmailStr]
    user: User
    worker: Optional[User]

    class Config:
        schema_extra = {
            "example": {
                "id": 4,
                "custom_name": "Fantastic Stack",
                "domains": ["rafsaf.pl", "registry.rafsaf.pl", "google.com"],
                "delay_between_checks": 10,
                "emails_to_alert": ["example@example.com"],
                "user": {
                    "id": 1,
                    "username": "example@example.com",
                    "full_name": "example@example.com",
                    "is_root": True,
                    "is_maintainer": False,
                    "is_worker": False,
                },
                "worker": {
                    "id": 10,
                    "username": "65e04ce6-4139-4e7c-9951-8712b84d6da6",
                    "full_name": None,
                    "is_root": False,
                    "is_maintainer": False,
                    "is_worker": True,
                },
            }
        }
        orm_mode = True


class HealthStackCreate(BaseModel):
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
