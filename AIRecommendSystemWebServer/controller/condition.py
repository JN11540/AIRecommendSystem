from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.condition import ConditionCreate, ConditionUpdate
from service.condition import ConditionService

router = APIRouter(prefix="/conditions", tags=["condition"])
svc = ConditionService()


@router.get("/")
async def list_conditions(db: AsyncSession = Depends(get_db)):
    return await svc.get_all(db)


@router.post("/")
async def create_condition(data: ConditionCreate, db: AsyncSession = Depends(get_db)):
    return await svc.create(db, data)


@router.get("/{condition_id}")
async def get_condition(condition_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.get(db, condition_id)


@router.put("/{condition_id}")
async def update_condition(condition_id: int, data: ConditionUpdate, db: AsyncSession = Depends(get_db)):
    return await svc.update(db, condition_id, data)


@router.delete("/{condition_id}")
async def delete_condition(condition_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.delete(db, condition_id)
