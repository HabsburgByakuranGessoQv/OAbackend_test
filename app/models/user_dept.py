from sqlalchemy import Table, Column, ForeignKey
from app.database import Base

user_dept_table = Table(
    "user_dept",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("dept_id", ForeignKey("departments.id"), primary_key=True)
)