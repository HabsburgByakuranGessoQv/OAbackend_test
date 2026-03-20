from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, services
from app.database import get_db
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=schemas.UserOut)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    - 接收用户名、密码和可选的全名
    - 返回新创建的用户信息（不含密码）
    """
    try:
        user = services.auth_service.register_user(db, user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user
    """
    return schemas.UserOut(
        id=1,
        username=user_in.username,
        full_name=user_in.full_name,
        is_active=True,
        role="employee"
    )
    """

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = services.auth_service.create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user