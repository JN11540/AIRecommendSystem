from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from model.condition import Condition
from schema.condition import ConditionCreate, ConditionUpdate


class CRUDCondition(CRUDBase[Condition, ConditionCreate, ConditionUpdate]):
    async def get_by_rule(self, db: AsyncSession, rule_id: int) -> list[Condition]:
        result = await db.execute(select(Condition).where(Condition.rule_id == rule_id))
        return list(result.scalars().all())
