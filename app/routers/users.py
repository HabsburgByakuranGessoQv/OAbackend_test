from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth.password import hash_password
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session, selectinload

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前登录用户的信息
    """
    return current_user


@router.get("/", response_model=List[schemas.UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 需要登录
) -> Any:
    """
    获取所有用户列表（分页）
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    根据 ID 获取单个用户
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

"""
@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
        user_in: schemas.UserCreate,
        db: Session = Depends(get_db),
) -> Any:
    # 检查用户名是否已存在
    existing = crud.user.get_by_username(db, username=user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 哈希密码
    hashed_password = hash_password(user_in.password)

    # 创建 ORM 实例（跳过 CRUD，因为 CRUD 的 create 方法期望传入完整的数据字典）
    db_user = User(
        username=user_in.username,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        # is_active 和 role 使用默认值
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""



"""
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    # 更新用户信息（仅允许本人或管理员）
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # 权限检查：本人或管理员
    if current_user.id != user_id and (not current_user.role or current_user.role.name != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    # 删除用户（仅管理员）
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = crud.user.remove(db, id=user_id)
    return user
"""
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新用户信息：
    - 如果更新角色（role字段），仅允许管理员操作
    - 如果更新其他字段，允许本人或管理员操作
    """
    # 获取要更新的用户
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 判断客户端是否试图修改 role 字段
    update_data = user_in.dict(exclude_unset=True)
    trying_to_update_role = 'role' in update_data

    if trying_to_update_role:
        # 修改角色需要管理员权限
        if not current_user.role or current_user.role.name != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can update role"
            )
    else:
        # 不修改角色，允许本人或管理员
        if current_user.id != user_id and (not current_user.role or current_user.role.name != "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    # 执行更新
    try:
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
    except ValueError as e:
        # 捕获角色不存在等业务逻辑错误，返回400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return user

"""
@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    # 检查当前用户是否有 admin 角色
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = crud.user.remove(db, id=user_id)
    return user
"""
"""
@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    # 检查当前用户是否有 admin 角色
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # 使用 options(selectinload()) 预先加载 role 关系
    user = db.query(User).options(selectinload(User.role)).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 执行删除
    db.delete(user)
    db.commit()

    # 返回被删除的用户对象（此时 role 数据已加载，不会触发延迟加载）
    return user
"""
@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 使用增强后的 get 方法预先加载 role
    user = crud.user.get(db, id=user_id, options=[selectinload(User.role)])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 使用 remove 方法（传入已加载好的对象）
    user = crud.user.remove(db, db_obj=user)
    return user
