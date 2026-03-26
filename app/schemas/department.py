from pydantic import BaseModel, ConfigDict
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
    # user_ids: List[int] = []   # 仅保留多对多关系下的用户 ID
    user_ids: List[int]  # 不再给默认值

    model_config = ConfigDict(from_attributes=True)