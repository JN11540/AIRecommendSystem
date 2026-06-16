from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    id: int | None = None


class ExerciseUpdate(BaseModel):
    name: str | None = None


class ExerciseResponse(ExerciseBase):
    id: int

    model_config = {"from_attributes": True}
