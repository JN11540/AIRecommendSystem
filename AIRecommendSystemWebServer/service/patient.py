from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.patient import CRUDPatient
from model.patient import Patient
from schema.patient import PatientCreate, PatientUpdate, PatientResponse


class PatientService:
    def __init__(self):
        self.crud = CRUDPatient(Patient)

    async def get(self, db: AsyncSession, patient_id: int) -> JSONResponse:
        obj = await self.crud.get(db, patient_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Patient not found")
        return await HttpResponseMethod.ok(data=PatientResponse.model_validate(obj).model_dump())

    async def get_all(self, db: AsyncSession) -> JSONResponse:
        objs = await self.crud.get_all(db)
        data = [PatientResponse.model_validate(o).model_dump() for o in objs]
        return await HttpResponseMethod.ok(data=data)

    async def create(self, db: AsyncSession, data: PatientCreate) -> JSONResponse:
        obj = await self.crud.create(db, data)
        return await HttpResponseMethod.ok(data=PatientResponse.model_validate(obj).model_dump())

    async def update(self, db: AsyncSession, patient_id: int, data: PatientUpdate) -> JSONResponse:
        obj = await self.crud.get(db, patient_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Patient not found")
        updated = await self.crud.update(db, obj, data)
        return await HttpResponseMethod.ok(data=PatientResponse.model_validate(updated).model_dump())

    async def delete(self, db: AsyncSession, patient_id: int) -> JSONResponse:
        obj = await self.crud.delete(db, patient_id)
        if not obj:
            return await HttpResponseMethod.not_found(message="Patient not found")
        return await HttpResponseMethod.ok(data=None)
