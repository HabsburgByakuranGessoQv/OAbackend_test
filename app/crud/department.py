from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Department | None:
        return db.query(self.model).filter(self.model.name == name).first()

department = CRUDDepartment(Department)