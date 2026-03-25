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


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 权限检查（略，保持不变）
    update_data = user_in.dict(exclude_unset=True)
    trying_to_update_role = 'role' in update_data
    if trying_to_update_role:
        if not current_user.role or current_user.role.name != "admin":
            raise HTTPException(status_code=403, detail="Only admin can update role")
    else:
        if current_user.id != user_id and (not current_user.role or current_user.role.name != "admin"):
            raise HTTPException(status_code=403, detail="Not enough permissions")

    # 执行更新
    try:
        user = crud.user.update(db, db_obj=user, obj_in=user_in, updated_by=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 重新查询并预加载关系，确保 departments 等字段可用
    stmt = select(User).where(User.id == user_id).options(
        selectinload(User.role),
        selectinload(User.departments)
    )
    user_full = db.execute(stmt).scalar_one()
    return user_full


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