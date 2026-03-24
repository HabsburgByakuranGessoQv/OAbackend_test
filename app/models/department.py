from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.user_dept import user_dept_table

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    # 关系
    manager: Mapped[Optional["User"]] = relationship(foreign_keys=[manager_id], post_update=True)
    # 注意：employees 关系使用 User.main_dept_id，这里用字符串引用 User
    employees: Mapped[List["User"]] = relationship(
        foreign_keys="User.main_dept_id",
        back_populates="main_dept"
    )
    # 多对多关系
    users: Mapped[List["User"]] = relationship(
        secondary=user_dept_table,
        back_populates="departments"
    )