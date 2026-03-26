from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app import crud, schemas
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models import Department
from app.models.user import User

router = APIRouter(prefix="/departments", tags=["departments"])


# 创建部门
@router.post("/create", response_model=schemas.DepartmentOut)
def create_department(
    dept_in: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    existing = crud.department.get_by_name(db, name=dept_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Department name already exists")
    dept = crud.department.create(db, obj_in=dept_in)
    return dept


# 获取部门列表（如有需要）
@router.get("/", response_model=List[schemas.DepartmentOut])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stmt = select(Department).offset(skip).limit(limit).order_by(Department.id).options(selectinload(Department.users))
    depts = db.execute(stmt).scalars().all()
    return depts

# 获取单个部门详情（预加载 users）
@router.get("/{dept_id}", response_model=schemas.DepartmentOut)
def read_department(dept_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Department).where(Department.id == dept_id).options(selectinload(Department.users))
    dept = db.execute(stmt).scalar_one_or_none()
    if not dept:
        raise HTTPException(404, "Department not found")
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

    # 先获取部门和用户对象
    department = db.get(Department, dept_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 检查用户是否属于该部门（使用多对多关系）
    if department not in user.departments:
        raise HTTPException(status_code=400, detail="User is not a member of this department")

    # 设置部门经理
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

    success = crud.department.add_employee(db, dept_id=dept_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=400, detail="User already in department")

    # 返回用户信息，预加载角色和部门关系
    stmt = select(User).where(User.id == user_id).options(
        selectinload(User.role),
        selectinload(User.departments)
    )
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 将用户从某个部门移除
@router.delete("/departments/{dept_id}/employees/{user_id}", response_model=schemas.UserOut)
def remove_employee_from_department(
        dept_id: int,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 1. 权限检查
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin required")

    # 2. 查询部门和用户（确保存在）
    department = db.get(Department, dept_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. 检查用户是否属于该部门
    if department not in user.departments:
        raise HTTPException(status_code=400, detail="User is not in this department")

    # 4. 移除关联（从 user.departments 中移除，SQLAlchemy 会自动处理中间表）
    user.departments.remove(department)

    # 5. 提交事务
    db.commit()
    # 注意：commit 后，user 对象仍持有原来的 departments 关系，但数据库已更新
    # 如果需要返回最新状态，可以刷新对象或重新查询
    db.refresh(user)  # 刷新后，user.departments 将不包含已删除的部门

    # 6. 返回被移除的用户信息（可选）
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
    # 查询部门下的所有用户，预加载角色和部门关系
    stmt = select(User).where(User.departments.any(id=dept_id)).options(
        selectinload(User.role),
        selectinload(User.departments)
    )
    employees = db.execute(stmt).scalars().all()
    return employees