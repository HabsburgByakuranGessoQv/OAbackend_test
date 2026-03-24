from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.role_permission import role_permission_table

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(200))

    permissions: Mapped[List["Permission"]] = relationship(
        secondary=role_permission_table,
        back_populates="roles"
    )