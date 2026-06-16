from pydantic import BaseModel, Field


class ConditionRow(BaseModel):
    rule_id: int = Field(gt=0)
    metric_id: int = Field(gt=0)
    exercises: list[int] = Field(min_length=1)
    value: list[str] = Field(min_length=1)


# ---------- condition standalone API ----------

class ConditionCreate(BaseModel):
    rule_id: int = Field(gt=0)
    metric_id: int = Field(gt=0)
    exercises: list[int] = Field(min_length=1)
    value: list[str] = Field(min_length=1)


class ConditionUpdate(BaseModel):
    rule_id: int | None = Field(default=None, gt=0)
    metric_id: int | None = Field(default=None, gt=0)
    exercises: list[int] | None = Field(default=None, min_length=1)
    value: list[str] | None = Field(default=None, min_length=1)


class ConditionResponse(BaseModel):
    id: int
    rule_id: int
    metric_id: int
    exercises: list[int]
    value: list[str]

    model_config = {"from_attributes": True}


# ---------- condition embedded inside Rule ----------

class ConditionInRuleCreate(BaseModel):
    metric_id: int = Field(gt=0)
    exercises: list[int] = Field(min_length=1)
    value: list[str] = Field(min_length=1)


class ConditionInRuleResponse(BaseModel):
    id: int
    metric_id: int
    exercises: list[int]
    value: list[str]

    model_config = {"from_attributes": True}
