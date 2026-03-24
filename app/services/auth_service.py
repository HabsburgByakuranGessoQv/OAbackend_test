from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.auth import password, jwt_handler
from app.schemas.user import UserOut

def register_user(db: Session, user_in: schemas.UserCreate):
    # 检查用户名是否已存在
    existing = crud.user.get_by_username(db, user_in.username)
    if existing:
        raise ValueError("Username already registered")

    # 获取默认角色
    default_role = db.query(models.Role).filter(models.Role.name == "employee").first()
    if not default_role:
        default_role = models.Role(name="employee", description="Regular employee")
        db.add(default_role)
        db.commit()
        db.refresh(default_role)

    # 哈希密码
    hashed_password = password.hash_password(user_in.password)

    # 创建用户
    db_user = models.User(
        username=user_in.username,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=default_role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 确保 role 关系已加载（可选，但安全）
    # 如果关系未加载，可以手动刷新
    if not hasattr(db_user, 'role') or db_user.role is None:
        db.refresh(db_user, attribute_names=['role'])

    # 显式转换为 UserOut，以利用 Pydantic 的 from_attributes 递归转换
    return UserOut.model_validate(db_user)


def authenticate_user(db: Session, username: str, password_plain: str):
    user = crud.user.get_by_username(db, username)
    if not user:
        return None
    if not password.verify_password(password_plain, user.hashed_password):
        return None
    return user

def create_access_token(user):
    role_name = user.role.name if user.role else "employee"  # 如果没有角色，给个默认
    data = {"sub": str(user.id), "username": user.username, "role": role_name}
    return jwt_handler.create_access_token(data)