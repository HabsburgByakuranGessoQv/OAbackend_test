from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from .role import role_permission  # 导入关联表

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)        # 权限代码，如 "user:delete"
    name = Column(String(100), nullable=False)                     # 权限显示名称

    # 多对多关系到角色
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")