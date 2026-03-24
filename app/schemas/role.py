from pydantic import BaseModel
from typing import Optional

class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True   # 允许从 SQLAlchemy 对象读取属性