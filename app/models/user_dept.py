from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

user_dept_table = Table(
    "user_dept",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("dept_id", Integer, ForeignKey("departments.id"), primary_key=True)
)