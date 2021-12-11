from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from app import schemas
from .. import deps
from app.core import security
from app.core.config import settings
from app.models import User
from sqlalchemy import select
import uuid
import secrets

router = APIRouter(prefix="/healthstack")


@router.post("/create", response_model=schemas.HealthStack)
async def login_access_token(
    stack_data: schemas.HealthStackCreate,
    session: AsyncSession = Depends(deps.get_session),
):
    print(stack_data)
