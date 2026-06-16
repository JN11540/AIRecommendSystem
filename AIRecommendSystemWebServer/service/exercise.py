import json

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.database import engine
from core.httpResponseMethod import HttpResponseMethod
from crud.exercise import CRUDExercise
from model.exercise import Exercise
from schema.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse

EXERCISE_JSON = settings.EXERCISE_JSON


class ExerciseService:
    def __init__(self):
        self.crud_exercise = CRUDExercise(Exercise)

    async def get(self, db: AsyncSession, exercise_id: int) -> JSONResponse:
        obj = await self.crud_exercise.get(db, exercise_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Exercise not found")
        return await HttpResponseMethod.ok(data=ExerciseResponse.model_validate(obj).model_dump())

    async def get_all(self, db: AsyncSession) -> JSONResponse:
        objs = await self.crud_exercise.get_all(db)
        data = [ExerciseResponse.model_validate(o).model_dump() for o in objs]
        return await HttpResponseMethod.ok(data=data)

    async def create(self, db: AsyncSession, data: ExerciseCreate) -> JSONResponse:
        obj = await self.crud_exercise.create(db, data)
        return await HttpResponseMethod.ok(data=ExerciseResponse.model_validate(obj).model_dump())

    async def update(self, db: AsyncSession, exercise_id: int, data: ExerciseUpdate) -> JSONResponse:
        obj = await self.crud_exercise.get(db, exercise_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Exercise not found")
        updated = await self.crud_exercise.update(db, obj, data)
        return await HttpResponseMethod.ok(data=ExerciseResponse.model_validate(updated).model_dump())

    async def delete(self, db: AsyncSession, exercise_id: int) -> JSONResponse:
        obj = await self.crud_exercise.delete(db, exercise_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Exercise not found")
        return await HttpResponseMethod.ok(data=ExerciseResponse.model_validate(obj).model_dump())

    async def seed_exercises(self) -> None:
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            existing = await self.crud_exercise.get_multi(session, limit=1)
            if existing:
                return

            with open(EXERCISE_JSON, encoding="utf-8") as f:
                exercises = json.load(f)

            exercises.sort(key=lambda x: x["id"])

            for item in exercises:
                await self.crud_exercise.create(session, obj_in=ExerciseCreate(
                    id=item["id"],
                    name=item["name"]
                ))
