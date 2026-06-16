from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class Patient(Base):
    __tablename__ = "patient"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    metric_values: Mapped[list] = mapped_column(JSON, nullable=False)
