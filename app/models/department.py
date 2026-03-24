from typing import Optional, List
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    manager: Mapped[Optional["User"]] = relationship(foreign_keys=[manager_id], post_update=True)
    employees: Mapped[List["User"]] = relationship(
        foreign_keys="User.main_dept_id",
        back_populates="main_dept"
    )
    users: Mapped[List["User"]] = relationship(
        secondary="user_dept",
        back_populates="departments"
    )