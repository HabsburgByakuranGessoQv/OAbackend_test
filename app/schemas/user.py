from pydantic import BaseModel, field_serializer
from typing import Optional, Any, List
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
    role: Any = None          # 使用 Any，通过序列化器处理
    main_dept_id: Optional[int] = None
    direct_leader_id: Optional[int] = None
    position: Optional[str] = None
    user_type: Optional[str] = None
    is_deleted: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    departments: Any = []     # 使用 Any，通过序列化器处理

    @field_serializer('role')
    def serialize_role(self, value: Any) -> Optional[dict]:
        """将 Role 对象转换为字典（符合 RoleOut 结构）"""
        if value is None:
            return None
        # 如果已经是 RoleOut 实例，直接返回
        if isinstance(value, RoleOut):
            return value.model_dump()
        # 如果是 SQLAlchemy Role 对象
        if hasattr(value, 'id') and hasattr(value, 'name'):
            return {"id": value.id, "name": value.name, "description": getattr(value, 'description', None)}
        return value

    @field_serializer('departments')
    def serialize_departments(self, value: Any) -> List[int]:
        if isinstance(value, list) and value and hasattr(value[0], 'id'):
            return [item.id for item in value]
        return []

    class Config:
        from_attributes = True