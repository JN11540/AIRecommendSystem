from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.rule import CRUDRule
from crud.condition import CRUDCondition
from model.rule import Rule
from model.condition import Condition
from schema.rule import RuleCreate, RuleUpdate, RuleResponse
from schema.condition import ConditionRow


class RuleService:
    def __init__(self):
        self.crud_rule = CRUDRule(Rule)
        self.crud_condition = CRUDCondition(Condition)

    async def get(self, db: AsyncSession, rule_id: int) -> JSONResponse:
        obj = await self.crud_rule.get(db, rule_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Rule not found")
        return await HttpResponseMethod.ok(data=RuleResponse.model_validate(obj).model_dump())

    async def get_all(self, db: AsyncSession) -> JSONResponse:
        objs = await self.crud_rule.get_all(db)
        data = [RuleResponse.model_validate(o).model_dump() for o in objs]
        return await HttpResponseMethod.ok(data=data)

    async def create(self, db: AsyncSession, data: RuleCreate) -> JSONResponse:
        rule = await self.crud_rule.create(db, data.model_copy(update={"conditions": []}))
        for cond in data.conditions:
            await self.crud_condition.create(db, ConditionRow(
                rule_id=rule.id,
                metric_id=cond.metric_id,
                exercises=cond.exercises,
                value=cond.value,
            ))
        obj = await self.crud_rule.get(db, rule.id)
        return await HttpResponseMethod.ok(data=RuleResponse.model_validate(obj).model_dump())

    async def update(self, db: AsyncSession, rule_id: int, data: RuleUpdate) -> JSONResponse:
        obj = await self.crud_rule.get(db, rule_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Rule not found")
        await self.crud_rule.update(db, obj, data.model_copy(update={"conditions": None}))
        if data.conditions is not None:
            for cond in await self.crud_condition.get_by_rule(db, rule_id):
                await self.crud_condition.delete(db, cond.id)
            for cond in data.conditions:
                await self.crud_condition.create(db, ConditionRow(
                    rule_id=rule_id,
                    metric_id=cond.metric_id,
                    exercises=cond.exercises,
                    value=cond.value,
                ))
        obj = await self.crud_rule.get(db, rule_id)
        return await HttpResponseMethod.ok(data=RuleResponse.model_validate(obj).model_dump())

    async def delete(self, db: AsyncSession, rule_id: int) -> JSONResponse:
        obj = await self.crud_rule.delete(db, rule_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Rule not found")
        return await HttpResponseMethod.ok(data=None)
