from typing import Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.auth.password import hash_password
from app.models.role import Role

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.username == username,
            self.model.is_deleted == False
        ).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed = hash_password(obj_in.password)
        db_obj = User(
            username=obj_in.username,
            hashed_password=hashed,
            full_name=obj_in.full_name,
            created_by=None,  # TODO: 从上下文获取当前用户
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # 处理角色字段
        role_name = update_data.pop('role', None)
        if role_name:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                raise ValueError(f"Role '{role_name}' does not exist")
            db_obj.role = role

        # 重要：移除 updated_at，并强制重置对象属性
        # update_data.pop('updated_at', None)


        # 更新普通字段
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # 手动设置 updated_by（暂无真实用户，设为 None 避免外键冲突）
        db_obj.updated_by = None

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
user = CRUDUser(User)