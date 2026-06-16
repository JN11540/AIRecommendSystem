from pydantic import BaseModel


class OperatorBase(BaseModel):
    name: str


class OperatorCreate(OperatorBase):
    id: int | None = None


class OperatorUpdate(BaseModel):
    name: str | None = None


class OperatorResponse(OperatorBase):
    id: int

    model_config = {"from_attributes": True}
