from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.operator import OperatorCreate, OperatorUpdate
from service.operator import OperatorService

router = APIRouter(prefix="/operators", tags=["operator"])
svc = OperatorService()


@router.get("/")
async def list_operators(db: AsyncSession = Depends(get_db)):
    return await svc.get_all(db)


@router.get("/{operator_id}")
async def get_operator(operator_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.get(db, operator_id)


@router.post("/")
async def create_operator(data: OperatorCreate, db: AsyncSession = Depends(get_db)):
    return await svc.create(db, data)


@router.put("/{operator_id}")
async def update_operator(operator_id: int, data: OperatorUpdate, db: AsyncSession = Depends(get_db)):
    return await svc.update(db, operator_id, data)


@router.delete("/{operator_id}")
async def delete_operator(operator_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.delete(db, operator_id)
