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

    # 唯一的多对多关系：users
    users: Mapped[List["User"]] = relationship(
        secondary=user_dept_table,
        back_populates="departments"
    )

    @property
    def user_ids(self) -> List[int]:
        # 返回该部门所有用户的 ID 列表
        # 注意：访问 self.users 可能触发懒加载，所以使用时最好预加载
        return [user.id for user in self.users]