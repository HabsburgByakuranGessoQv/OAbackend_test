from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)   # 新增外键
    # 使用 server_default 让数据库自动填充当前时间
    created_at = Column(DateTime, server_default=func.now())
    # 关系示例：一个用户有多条考勤记录
    attendances = relationship("Attendance", back_populates="user")
    role = relationship("Role", backref="users")  # 每个用户属于一个角色