from crud.base import CRUDBase
from model.metric import Metric
from schema.metric import MetricCreate, MetricUpdate


class CRUDMetric(CRUDBase[Metric, MetricCreate, MetricUpdate]):
    pass
