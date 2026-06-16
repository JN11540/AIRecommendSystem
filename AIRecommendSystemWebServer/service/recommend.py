from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.httpResponseMethod import HttpResponseMethod
from crud.metric import CRUDMetric
from crud.patient import CRUDPatient
from crud.rule import CRUDRule
from model.metric import Metric
from model.patient import Patient
from model.rule import Rule
from schema.rule import RecommendRequest

_OPS = {'>=', '>', '<=', '<', '='}


def _match(value: list[str], input_str: str) -> bool:
    try:
        v_in = float(input_str)
        if len(value) == 2 and value[0] in _OPS:
            op, thr = value[0], float(value[1])
            if op == '>=': return v_in >= thr
            if op == '>':  return v_in > thr
            if op == '<=': return v_in <= thr
            if op == '<':  return v_in < thr
            return v_in == thr
        if len(value) == 1:
            return v_in == float(value[0])
        lo = min(float(v) for v in value)
        hi = max(float(v) for v in value)
        return lo <= v_in <= hi
    except (ValueError, TypeError):
        return False


class RecommendService:
    def __init__(self):
        self.crud_rule = CRUDRule(Rule)
        self.crud_patient = CRUDPatient(Patient)
        self.crud_metric = CRUDMetric(Metric)

    async def recommend(self, db: AsyncSession, req: RecommendRequest) -> JSONResponse:
        # 1. 取得病患
        patient = await self.crud_patient.get(db, req.patient_id)
        if not patient:
            return await HttpResponseMethod.not_found(message="Patient not found")

        # 2. 取得所有指標（依 id 排序），對應 metric_values 的順序
        all_metrics = sorted(await self.crud_metric.get_all(db), key=lambda m: m.id)
        if len(patient.metric_values) < len(all_metrics):
            return await HttpResponseMethod.bad_request(
                message="Patient metric_values count does not match metrics count"
            )
        metric_map: dict[int, str] = {
            m.id: patient.metric_values[i] for i, m in enumerate(all_metrics)
        }

        # 3. 取得指定規則
        rule = await self.crud_rule.get(db, req.rule_id)
        if not rule:
            return await HttpResponseMethod.not_found(message="Rule not found")

        # 4. 決策樹演算法
        conditions = sorted(rule.conditions, key=lambda c: c.id)

        # 依 metric_id 分組，保留第一次出現的順序（即決策樹層序）
        layers: dict[int, list] = {}
        for cond in conditions:
            layers.setdefault(cond.metric_id, []).append(cond)

        matched = []
        for metric_id, layer_conds in layers.items():
            if metric_id not in metric_map:
                return await HttpResponseMethod.bad_request(
                    message=f"Missing value for metric_id {metric_id}"
                )
            hit = next(
                (c for c in layer_conds if _match(c.value, metric_map[metric_id])),
                None,
            )
            if hit is None:
                # 此層無分支命中，無推薦結果
                return await HttpResponseMethod.ok(data={"recommended": []})
            matched.append(hit)

        if not matched:
            return await HttpResponseMethod.ok(data={"recommended": []})

        # 5. 取所有命中條件的 exercises 交集
        path_ex: set[int] = set(matched[0].exercises)
        for m in matched[1:]:
            path_ex &= set(m.exercises)

        return await HttpResponseMethod.ok(data={"recommended": sorted(path_ex)})
