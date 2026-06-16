from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schema.patient import PatientCreate, PatientUpdate
from service.patient import PatientService

router = APIRouter(prefix="/patients", tags=["patient"])
svc = PatientService()


@router.get("/")
async def list_patients(db: AsyncSession = Depends(get_db)):
    return await svc.get_all(db)


@router.get("/{patient_id}")
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.get(db, patient_id)


@router.post("/")
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await svc.create(db, data)


@router.put("/{patient_id}")
async def update_patient(patient_id: int, data: PatientUpdate, db: AsyncSession = Depends(get_db)):
    return await svc.update(db, patient_id, data)


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await svc.delete(db, patient_id)
