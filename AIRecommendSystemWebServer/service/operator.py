import json

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.database import engine
from core.httpResponseMethod import HttpResponseMethod
from crud.operator import CRUDOperator
from model.operator import Operator
from schema.operator import OperatorCreate, OperatorUpdate, OperatorResponse

OPERATOR_JSON = settings.OPERATOR_JSON


class OperatorService:
    def __init__(self):
        self.crud_operator = CRUDOperator(Operator)

    async def get(self, db: AsyncSession, operator_id: int) -> JSONResponse:
        obj = await self.crud_operator.get(db, operator_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Operator not found")
        return await HttpResponseMethod.ok(data=OperatorResponse.model_validate(obj).model_dump())

    async def get_all(self, db: AsyncSession) -> JSONResponse:
        objs = await self.crud_operator.get_all(db)
        data = [OperatorResponse.model_validate(o).model_dump() for o in objs]
        return await HttpResponseMethod.ok(data=data)

    async def create(self, db: AsyncSession, data: OperatorCreate) -> JSONResponse:
        obj = await self.crud_operator.create(db, data)
        return await HttpResponseMethod.ok(data=OperatorResponse.model_validate(obj).model_dump())

    async def update(self, db: AsyncSession, operator_id: int, data: OperatorUpdate) -> JSONResponse:
        obj = await self.crud_operator.get(db, operator_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Operator not found")
        updated = await self.crud_operator.update(db, obj, data)
        return await HttpResponseMethod.ok(data=OperatorResponse.model_validate(updated).model_dump())

    async def delete(self, db: AsyncSession, operator_id: int) -> JSONResponse:
        obj = await self.crud_operator.delete(db, operator_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Operator not found")
        return await HttpResponseMethod.ok(data=OperatorResponse.model_validate(obj).model_dump())

    async def seed_operators(self) -> None:
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            existing = await self.crud_operator.get_multi(session, limit=1)
            if existing:
                return

            with open(OPERATOR_JSON, encoding="utf-8") as f:
                operators = json.load(f)

            operators.sort(key=lambda x: x["id"])

            for item in operators:
                await self.crud_operator.create(session, obj_in=OperatorCreate(
                    id=item["id"],
                    name=item["name"]
                ))
