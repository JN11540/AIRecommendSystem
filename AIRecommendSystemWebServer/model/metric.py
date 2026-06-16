from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class Metric(Base):
    __tablename__ = "metric"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
