from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    name: Optional[str] = None

class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        from_attributes = True