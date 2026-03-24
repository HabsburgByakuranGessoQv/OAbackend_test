from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime)
    status = Column(String(20), default="present")  # present, absent, leave, etc.

    # 关系：多个考勤记录属于一个用户
    # user = relationship("User", back_populates="attendances")
