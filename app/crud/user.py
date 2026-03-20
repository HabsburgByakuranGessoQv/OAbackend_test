from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.role import Role  # 导入 Role 模型
from app.schemas.user import UserCreate, UserUpdate
from typing import Union, Dict, Any

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        # 如果传入的是 UserUpdate 对象，转换为字典（排除未设置的字段）
        if isinstance(obj_in, UserUpdate):
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = obj_in

        # 单独处理角色字段：将角色名转换为 Role 对象
        role_name = update_data.pop('role', None)
        if role_name:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                raise ValueError(f"Role '{role_name}' does not exist")
            db_obj.role = role  # 直接赋值 relationship 对象

        # 调用父类方法更新剩余字段
        return super().update(db, db_obj=db_obj, obj_in=update_data)

# 创建 CRUD 实例，供其他地方导入使用
user = CRUDUser(User)