from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app import models, schemas
from app.api import deps

router = APIRouter(prefix="/healthstack")


@router.post("/create", response_model=schemas.HealthStack)
async def create_healthstack(
    stack_data: schemas.HealthStackCreate,
    current_user: models.User = Depends(deps.get_normal_user),
    session: AsyncSession = Depends(deps.get_session),
):
    new_healthstack = models.HealthStack(
        custom_name=stack_data.custom_name,
        emails_to_alert=stack_data.emails_to_alert,
        domains=stack_data.domains,
        delay_between_checks=stack_data.delay_between_checks,
        user=current_user,
    )
    session.add(new_healthstack)
    await session.commit()
    await session.refresh(new_healthstack)
    return new_healthstack


@router.get("", response_model=list[schemas.HealthStack])
async def get_all_health_stacks(
    offset: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_maintainer_user),
    session: AsyncSession = Depends(deps.get_session),
):
    users_result = await session.execute(
        select(models.HealthStack)
        .offset(offset)
        .limit(limit)
        .options(joinedload("user"))
        .options(joinedload("worker"))
    )
    return users_result.scalars().all()


@router.get("/me", response_model=list[schemas.HealthStack])
async def get_all_my_health_stacks(
    offset: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_normal_user),
    session: AsyncSession = Depends(deps.get_session),
):
    users_result = await session.execute(
        select(models.HealthStack)
        .where(models.HealthStack.user_id == current_user.id)
        .offset(offset)
        .limit(limit)
        .options(joinedload("user"))
        .options(joinedload("worker"))
    )
    return users_result.scalars().all()


@router.get("/me/{id}", response_model=schemas.HealthStack)
async def get_my_healthstack_by_id(
    id: int,
    current_user: models.User = Depends(deps.get_normal_user),
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(
        select(models.HealthStack)
        .where(models.HealthStack.user == current_user, models.HealthStack.id == id)
        .options(joinedload("user"))
        .options(joinedload("worker"))
    )
    healthstack = result.scalars().first()
    if healthstack is None:
        return JSONResponse(
            status_code=404,
            content={"message": "HealthStack not found"},
        )
    return healthstack


@router.get("/{id}", response_model=schemas.HealthStack)
async def get_healthstack_by_id(
    id: int,
    current_user: models.User = Depends(deps.get_maintainer_user),
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(
        select(models.HealthStack)
        .where(models.HealthStack.id == id)
        .options(joinedload("user"))
        .options(joinedload("worker"))
    )
    healthstack = result.scalars().first()
    if healthstack is None:
        return JSONResponse(
            status_code=404,
            content={"message": "HealthStack not found"},
        )
    return healthstack


@router.get("/worker/me/{id}", response_model=schemas.HealthStack)
async def get_worker_me_healthstack_by_id(
    id: int,
    current_user: models.User = Depends(deps.get_worker_user),
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(
        select(models.HealthStack)
        .where(models.HealthStack.worker == current_user, models.HealthStack.id == id)
        .options(joinedload("user"))
        .options(joinedload("worker"))
    )
    healthstack = result.scalars().first()
    if healthstack is None:
        return JSONResponse(
            status_code=404,
            content={"message": "HealthStack not found"},
        )
    return healthstack
