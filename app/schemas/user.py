from pydantic import BaseModel
from typing import Optional

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

class UserOut(UserBase):
    id: int
    is_active: bool
    role: Optional[RoleOut] = None  # 改为 RoleOut 类型

    class Config:
        from_attributes = True