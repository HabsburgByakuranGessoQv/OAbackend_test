from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.role_permission import role_permission_table

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permission_table,
        back_populates="permissions"
    )