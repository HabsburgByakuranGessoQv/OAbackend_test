from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app import crud, schemas
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: User = Depends(get_current_user)) -> Any:
    return current_user


@router.get("/all/", response_model=list[schemas.UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 添加 order_by
    stmt = select(User).order_by(User.id).offset(skip).limit(limit)
    users = db.execute(stmt).scalars().all()
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    user = crud.user.get(db, id=user_id, options=[selectinload(User.role), selectinload(User.departments)])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. 权限检查（示例：仅本人或管理员可修改）
    if current_user.id != user_id and (not current_user.role or current_user.role.name != "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 2. 获取要更新的用户对象
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. 处理直属上级字段
    direct_leader_id = user_in.direct_leader_id
    if direct_leader_id is not None:
        # 前端可能用 0 表示“清空”，转换为 None
        if direct_leader_id == 0:
            direct_leader_id = None
        else:
            # 检查直属上级用户是否存在
            leader = crud.user.get(db, id=direct_leader_id)
            if not leader:
                raise HTTPException(status_code=400, detail="Direct leader not found")
            # 可选：防止自引用
            if direct_leader_id == user_id:
                raise HTTPException(status_code=400, detail="User cannot be their own direct leader")
        # 将处理后的值赋回
        user_in.direct_leader_id = direct_leader_id

    # 4. 执行更新（CRUD 中应正确处理 None）
    user = crud.user.update(db, db_obj=user, obj_in=user_in, updated_by=current_user.id)
    return user


@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 获取用户并预加载 role 和 departments（删除后返回对象，需要这些关系）
    user = crud.user.get(db, id=user_id, options=[selectinload(User.role), selectinload(User.departments)])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = crud.user.remove(db, db_obj=user)
    return user