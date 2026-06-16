from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import model  # noqa: F401 — registers all ORM models before create_all
from core.config import STATIC_DIR
from core.database import Base, engine
from service.exercise import ExerciseService
from service.metric import MetricService
from service.operator import OperatorService
from controller.exercise import router as exercise_router
from controller.metric import router as metric_router
from controller.operator import router as operator_router
from controller.condition import router as condition_router
from controller.rule import router as rule_router
from controller.patient import router as patient_router
from controller.template import router as template_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await ExerciseService().seed_exercises()
    await MetricService().seed_metrics()
    await OperatorService().seed_operators()
    yield


app = FastAPI(title="AI Recommend System", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(template_router)
app.include_router(exercise_router)
app.include_router(metric_router)
app.include_router(operator_router)
app.include_router(rule_router)
app.include_router(condition_router)
app.include_router(patient_router)
