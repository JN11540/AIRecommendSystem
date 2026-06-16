from crud.base import CRUDBase
from model.operator import Operator
from schema.operator import OperatorCreate, OperatorUpdate


class CRUDOperator(CRUDBase[Operator, OperatorCreate, OperatorUpdate]):
    pass
