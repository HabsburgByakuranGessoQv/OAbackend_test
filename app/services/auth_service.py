from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.auth import password, jwt_handler

def register_user(db: Session, user_in: schemas.UserCreate):
    """
    # 检查用户是否存在
    existing = crud.user.get_by_username(db, user_in.username)
    if existing:
        raise ValueError("Username already registered")
    # 哈希密码
    hashed = password.hash_password(user_in.password)
    # 创建用户
    user_data = user_in.dict(exclude={"password"})
    # user_data = user_in.dict()
    user_data["hashed_password"] = hashed
    user = crud.user.create(db, schemas.UserCreate(**user_data))
    return user
    """
    """
    注册新用户
    - 检查用户名是否已存在
    - 哈希密码
    - 直接创建 ORM 模型实例并提交
    """
    # 检查用户名是否已存在
    existing = crud.user.get_by_username(db, user_in.username)
    if existing:
        raise ValueError("Username already registered")

    # 获取默认角色（例如 "employee"）
    default_role = db.query(models.Role).filter(models.Role.name == "employee").first()
    if not default_role:
        # 如果数据库中还没有 employee 角色，可以创建一个，或者抛出异常
        # 这里简单起见，我们创建一个（实际应该在初始化时创建）
        default_role = models.Role(name="employee", description="Regular employee")
        db.add(default_role)
        db.commit()  # 先提交以获取 ID
        db.refresh(default_role)

    # 哈希密码
    hashed_password = password.hash_password(user_in.password)

    # 直接创建 ORM 模型实例（不经过 CRUD 的 create 方法）
    db_user = models.User(
        username=user_in.username,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        # is_active 和 role 使用模型定义的默认值
        role_id=default_role.id  # 设置角色 ID
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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