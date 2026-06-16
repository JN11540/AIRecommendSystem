from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.condition import CRUDCondition
from model.condition import Condition
from schema.condition import ConditionCreate, ConditionRow, ConditionUpdate, ConditionResponse


class ConditionService:
    def __init__(self):
        self.crud = CRUDCondition(Condition)

    async def get(self, db: AsyncSession, condition_id: int) -> JSONResponse:
        obj = await self.crud.get(db, condition_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Condition not found")
        return await HttpResponseMethod.ok(data=ConditionResponse.model_validate(obj).model_dump())

    async def get_all(self, db: AsyncSession) -> JSONResponse:
        objs = await self.crud.get_all(db)
        data = [ConditionResponse.model_validate(o).model_dump() for o in objs]
        return await HttpResponseMethod.ok(data=data)

    async def create(self, db: AsyncSession, data: ConditionCreate) -> JSONResponse:
        obj = await self.crud.create(db, ConditionRow(**data.model_dump()))
        return await HttpResponseMethod.ok(data=ConditionResponse.model_validate(obj).model_dump())

    async def update(self, db: AsyncSession, condition_id: int, data: ConditionUpdate) -> JSONResponse:
        obj = await self.crud.get(db, condition_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Condition not found")
        updated = await self.crud.update(db, obj, data)
        return await HttpResponseMethod.ok(data=ConditionResponse.model_validate(updated).model_dump())

    async def delete(self, db: AsyncSession, condition_id: int) -> JSONResponse:
        obj = await self.crud.delete(db, condition_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Condition not found")
        return await HttpResponseMethod.ok(data=ConditionResponse.model_validate(obj).model_dump())
