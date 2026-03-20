from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# 角色-权限关联表
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)          # 角色名称，如 "admin", "employee"
    description = Column(String(200), nullable=True)                # 可选描述

    # 多对多关系到权限
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")