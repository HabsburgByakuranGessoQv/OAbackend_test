from sqlalchemy import select, insert, delete, func
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.department import Department
from app.models.user_dept import user_dept_table
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from typing import Optional, List

class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Department]:
        stmt = select(self.model).where(self.model.name == name)
        return db.execute(stmt).scalar_one_or_none()

    def add_employee(self, db: Session, dept_id: int, user_id: int) -> bool:
        """将用户添加到部门，返回是否成功"""
        # 检查是否已存在
        check_stmt = select(user_dept_table).where(
            user_dept_table.c.user_id == user_id,
            user_dept_table.c.dept_id == dept_id
        )
        if db.execute(check_stmt).first():
            return False
        ins = insert(user_dept_table).values(user_id=user_id, dept_id=dept_id)
        db.execute(ins)
        db.commit()
        return True

    def remove_employee(self, db: Session, dept_id: int, user_id: int) -> bool:
        """将用户从部门移除"""
        stmt = delete(user_dept_table).where(
            user_dept_table.c.user_id == user_id,
            user_dept_table.c.dept_id == dept_id
        )
        result = db.execute(stmt)
        db.commit()
        return result.rowcount > 0

    def get_user_depts(self, db: Session, user_id: int) -> List[int]:
        """获取用户所属部门ID列表"""
        stmt = select(user_dept_table.c.dept_id).where(user_dept_table.c.user_id == user_id)
        return [row[0] for row in db.execute(stmt).all()]

    def get_dept_users(self, db: Session, dept_id: int) -> List[int]:
        """获取部门下的用户ID列表"""
        stmt = select(user_dept_table.c.user_id).where(user_dept_table.c.dept_id == dept_id)
        return [row[0] for row in db.execute(stmt).all()]

    def assign_manager(self, db: Session, dept_id: int, manager_id: int) -> Optional[Department]:
        """设置部门经理"""
        dept = self.get(db, id=dept_id)
        if not dept:
            return None
        dept.manager_id = manager_id
        db.commit()
        db.refresh(dept)
        return dept

department = CRUDDepartment(Department)