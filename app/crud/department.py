from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.department import Department
from app.models.user_dept import user_dept_table
from app.schemas.department import DepartmentCreate, DepartmentUpdate

class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Department]:
        return db.query(self.model).filter(self.model.name == name).first()

    def add_user_to_dept(self, db: Session, dept_id: int, user_id: int):
        stmt = user_dept_table.insert().values(user_id=user_id, dept_id=dept_id)
        db.execute(stmt)
        db.commit()

    def remove_user_from_dept(self, db: Session, dept_id: int, user_id: int):
        stmt = user_dept_table.delete().where(
            user_dept_table.c.user_id == user_id,
            user_dept_table.c.dept_id == dept_id
        )
        db.execute(stmt)
        db.commit()

    def get_user_depts(self, db: Session, user_id: int) -> List[int]:
        result = db.query(user_dept_table.c.dept_id).filter(user_dept_table.c.user_id == user_id).all()
        return [r[0] for r in result]

    def get_dept_users(self, db: Session, dept_id: int) -> List[int]:
        result = db.query(user_dept_table.c.user_id).filter(user_dept_table.c.dept_id == dept_id).all()
        return [r[0] for r in result]

department = CRUDDepartment(Department)