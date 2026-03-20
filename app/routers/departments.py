from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/", response_model=List[schemas.DepartmentOut])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 需要登录
) -> Any:
    """
    获取所有部门列表
    """
    departments = crud.department.get_multi(db, skip=skip, limit=limit)
    return departments


@router.get("/{dept_id}", response_model=schemas.DepartmentOut)
def read_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    根据 ID 获取单个部门
    """
    department = crud.department.get(db, id=dept_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return department


@router.post("/", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    dept_in: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    创建新部门（仅管理员）
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 检查部门名是否已存在
    existing = crud.department.get_by_name(db, name=dept_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name already exists"
        )
    department = crud.department.create(db, obj_in=dept_in)
    return department


@router.put("/{dept_id}", response_model=schemas.DepartmentOut)
def update_department(
    dept_id: int,
    dept_in: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新部门信息（仅管理员）
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    department = crud.department.get(db, id=dept_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    # 如果更新名称且与其他部门冲突
    if dept_in.name and dept_in.name != department.name:
        existing = crud.department.get_by_name(db, name=dept_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department name already exists"
            )
    department = crud.department.update(db, db_obj=department, obj_in=dept_in)
    return department


@router.delete("/{dept_id}", response_model=schemas.DepartmentOut)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    删除部门（仅管理员）
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    department = crud.department.get(db, id=dept_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    department = crud.department.remove(db, id=dept_id)
    return department