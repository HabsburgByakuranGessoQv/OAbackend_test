from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/departments", tags=["departments"])

# 创建部门
@router.post("/", response_model=schemas.DepartmentOut)
def create_department(
    dept_in: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 可选：只有管理员才能创建部门
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    # 检查部门名是否已存在
    existing = crud.department.get_by_name(db, name=dept_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Department name already exists")
    dept = crud.department.create(db, obj_in=dept_in)
    return dept

# 获取部门列表
@router.get("/", response_model=List[schemas.DepartmentOut])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    depts = crud.department.get_multi(db, skip=skip, limit=limit)
    return depts

# 获取单个部门详情
@router.get("/{dept_id}", response_model=schemas.DepartmentOut)
def read_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = crud.department.get(db, id=dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

# 更新部门信息
@router.put("/{dept_id}", response_model=schemas.DepartmentOut)
def update_department(
    dept_id: int,
    dept_in: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    dept = crud.department.get(db, id=dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    dept = crud.department.update(db, db_obj=dept, obj_in=dept_in)
    return dept

# 删除部门
@router.delete("/{dept_id}", response_model=schemas.DepartmentOut)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    dept = crud.department.get(db, id=dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    dept = crud.department.remove(db, id=dept_id)
    return dept

# 设置部门经理
@router.post("/{dept_id}/manager/{user_id}", response_model=schemas.DepartmentOut)
def set_manager(
    dept_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    # 可选：检查用户是否属于该部门
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.department_id != dept_id:
        raise HTTPException(status_code=400, detail="User is not a member of this department")
    dept = crud.department.assign_manager(db, dept_id=dept_id, manager_id=user_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

# 将用户添加到部门
@router.post("/{dept_id}/employees/{user_id}", response_model=schemas.UserOut)
def add_employee(
    dept_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    user = crud.department.add_employee(db, dept_id=dept_id, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User or department not found")
    return user

# 将用户从部门移除
@router.delete("/employees/{user_id}", response_model=schemas.UserOut)
def remove_employee(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    user = crud.department.remove_employee(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 获取部门的所有员工
@router.get("/{dept_id}/employees", response_model=List[schemas.UserOut])
def get_employees(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = crud.department.get(db, id=dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    # 直接通过关系获取，或查询 User 表
    employees = db.query(User).filter(User.department_id == dept_id).all()
    return employees