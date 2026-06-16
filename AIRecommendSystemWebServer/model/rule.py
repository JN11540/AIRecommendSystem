from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base


class Rule(Base):
    __tablename__ = "rule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    conditions: Mapped[list["Condition"]] = relationship(  # noqa: F821
        "Condition", back_populates="rule", cascade="all, delete-orphan", lazy="selectin"
    )
