import json

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.database import engine
from core.httpResponseMethod import HttpResponseMethod
from crud.metric import CRUDMetric
from model.metric import Metric
from schema.metric import MetricCreate, MetricUpdate, MetricResponse

METRIC_JSON = settings.METRIC_JSON


class MetricService:
    def __init__(self):
        self.crud_metric = CRUDMetric(Metric)

    async def get(self, db: AsyncSession, metric_id: int) -> JSONResponse:
        obj = await self.crud_metric.get(db, metric_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Metric not found")
        return await HttpResponseMethod.ok(data=MetricResponse.model_validate(obj).model_dump())

    async def get_all(self, db: AsyncSession) -> JSONResponse:
        objs = await self.crud_metric.get_all(db)
        data = [MetricResponse.model_validate(o).model_dump() for o in objs]
        return await HttpResponseMethod.ok(data=data)

    async def create(self, db: AsyncSession, data: MetricCreate) -> JSONResponse:
        obj = await self.crud_metric.create(db, data)
        return await HttpResponseMethod.ok(data=MetricResponse.model_validate(obj).model_dump())

    async def update(self, db: AsyncSession, metric_id: int, data: MetricUpdate) -> JSONResponse:
        obj = await self.crud_metric.get(db, metric_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Metric not found")
        updated = await self.crud_metric.update(db, obj, data)
        return await HttpResponseMethod.ok(data=MetricResponse.model_validate(updated).model_dump())

    async def delete(self, db: AsyncSession, metric_id: int) -> JSONResponse:
        obj = await self.crud_metric.delete(db, metric_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Metric not found")
        return await HttpResponseMethod.ok(data=MetricResponse.model_validate(obj).model_dump())

    async def seed_metrics(self) -> None:
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            existing = await self.crud_metric.get_multi(session, limit=1)
            if existing:
                return

            with open(METRIC_JSON, encoding="utf-8") as f:
                metrics = json.load(f)

            metrics.sort(key=lambda x: x["id"])

            for item in metrics:
                await self.crud_metric.create(session, obj_in=MetricCreate(
                    id=item["id"],
                    name=item["name"]
                ))
