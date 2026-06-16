from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    name: str
    metric_values: list[str] = Field(min_length=1)


class PatientUpdate(BaseModel):
    name: str | None = None
    metric_values: list[str] | None = Field(default=None, min_length=1)


class PatientResponse(BaseModel):
    id: int
    name: str
    metric_values: list[str]

    model_config = {"from_attributes": True}
