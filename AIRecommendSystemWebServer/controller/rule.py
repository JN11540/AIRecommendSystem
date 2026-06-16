from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.rule import RuleCreate, RuleUpdate, RecommendRequest
from service.rule import RuleService
from service.recommend import RecommendService

router = APIRouter(prefix="/rules", tags=["rule"])
svc = RuleService()
recommend_svc = RecommendService()


@router.get("/")
async def list_rules(db: AsyncSession = Depends(get_db)):
    return await svc.get_all(db)


@router.post("/")
async def create_rule(data: RuleCreate, db: AsyncSession = Depends(get_db)):
    return await svc.create(db, data)


@router.get("/{rule_id}")
async def get_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.get(db, rule_id)


@router.put("/{rule_id}")
async def update_rule(rule_id: int, data: RuleUpdate, db: AsyncSession = Depends(get_db)):
    return await svc.update(db, rule_id, data)


@router.delete("/{rule_id}")
async def delete_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.delete(db, rule_id)


@router.post("/recommend")
async def recommend(data: RecommendRequest, db: AsyncSession = Depends(get_db)):
    return await recommend_svc.recommend(db, data)
