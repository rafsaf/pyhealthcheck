from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas

from .. import deps

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
