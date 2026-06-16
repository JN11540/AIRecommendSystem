from sqlalchemy import ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base


class Condition(Base):
    __tablename__ = "condition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rule_id: Mapped[int] = mapped_column(Integer, ForeignKey("rule.id"), nullable=False)
    metric_id: Mapped[int] = mapped_column(Integer, ForeignKey("metric.id"), nullable=False)
    exercises: Mapped[list] = mapped_column(JSON, nullable=False)
    value: Mapped[list] = mapped_column(JSON, nullable=False)

    rule: Mapped["Rule"] = relationship("Rule", back_populates="conditions")  # noqa: F821
    metric: Mapped["Metric"] = relationship("Metric", lazy="selectin")  # noqa: F821
