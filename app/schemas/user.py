from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.role import RoleOut

class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
    main_dept_id: Optional[int] = None
    direct_leader_id: Optional[int] = None
    position: Optional[str] = None
    user_type: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    # role: Optional[object] = None   # 根据之前定义，可能是对象或字符串，此处可保持灵活
    role: Optional[RoleOut] = None   # 确保是 RoleOut 类型
    main_dept_id: Optional[int] = None
    direct_leader_id: Optional[int] = None
    position: Optional[str] = None
    user_type: Optional[str] = None
    is_deleted: bool
    created_at: datetime
    # updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    departments: List[int] = []      # 部门ID列表，用于多对多（可选）

    class Config:
        from_attributes = True