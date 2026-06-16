from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class Operator(Base):
    __tablename__ = "operator"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
