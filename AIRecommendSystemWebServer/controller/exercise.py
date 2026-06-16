from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.exercise import ExerciseCreate, ExerciseUpdate
from service.exercise import ExerciseService

router = APIRouter(prefix="/exercises", tags=["exercise"])
svc = ExerciseService()


@router.get("/")
async def list_exercises(db: AsyncSession = Depends(get_db)):
    return await svc.get_all(db)


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.get(db, exercise_id)


@router.post("/")
async def create_exercise(data: ExerciseCreate, db: AsyncSession = Depends(get_db)):
    return await svc.create(db, data)


@router.put("/{exercise_id}")
async def update_exercise(exercise_id: int, data: ExerciseUpdate, db: AsyncSession = Depends(get_db)):
    return await svc.update(db, exercise_id, data)


@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.delete(db, exercise_id)
