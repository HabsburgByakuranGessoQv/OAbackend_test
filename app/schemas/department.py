from pydantic import BaseModel
from typing import Optional, List

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentOut(DepartmentBase):
    id: int
    manager_id: Optional[int] = None
    user_ids: List[int] = []          # 多对多用户ID列表
    employee_ids: List[int] = []      # 主要部门用户ID列表

    class Config:
        from_attributes = True