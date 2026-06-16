from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.metric import MetricCreate, MetricUpdate
from service.metric import MetricService

router = APIRouter(prefix="/metrics", tags=["metric"])
svc = MetricService()


@router.get("/")
async def list_metrics(db: AsyncSession = Depends(get_db)):
    return await svc.get_all(db)


@router.get("/{metric_id}")
async def get_metric(metric_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.get(db, metric_id)


@router.post("/")
async def create_metric(data: MetricCreate, db: AsyncSession = Depends(get_db)):
    return await svc.create(db, data)


@router.put("/{metric_id}")
async def update_metric(metric_id: int, data: MetricUpdate, db: AsyncSession = Depends(get_db)):
    return await svc.update(db, metric_id, data)


@router.delete("/{metric_id}")
async def delete_metric(metric_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.delete(db, metric_id)
