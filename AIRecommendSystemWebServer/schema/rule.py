from pydantic import BaseModel

from schema.condition import ConditionInRuleCreate, ConditionInRuleResponse


class RuleBase(BaseModel):
    name: str


class RuleCreate(RuleBase):
    conditions: list[ConditionInRuleCreate] = []


class RuleUpdate(BaseModel):
    name: str | None = None
    conditions: list[ConditionInRuleCreate] | None = None


class RuleResponse(RuleBase):
    id: int
    conditions: list[ConditionInRuleResponse] = []

    model_config = {"from_attributes": True}


class RecommendRequest(BaseModel):
    rule_id: int
    patient_id: int
