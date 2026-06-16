from pydantic import BaseModel


class MetricBase(BaseModel):
    name: str


class MetricCreate(MetricBase):
    id: int | None = None


class MetricUpdate(BaseModel):
    name: str | None = None


class MetricResponse(MetricBase):
    id: int

    model_config = {"from_attributes": True}
