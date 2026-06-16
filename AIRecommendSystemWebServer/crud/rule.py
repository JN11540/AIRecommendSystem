from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from model.rule import Rule
from schema.rule import RuleCreate, RuleUpdate


class CRUDRule(CRUDBase[Rule, RuleCreate, RuleUpdate]):
    async def get_all(self, db: AsyncSession) -> list[Rule]:
        result = await db.execute(select(Rule).order_by(Rule.name))
        return list(result.scalars().all())
