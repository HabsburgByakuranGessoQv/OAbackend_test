from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.auth.jwt_handler import decode_token
from app.models.user import User

# OAuth2 密码流，tokenUrl 应指向登录接口的路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    从 JWT 令牌中解析当前用户，注入到依赖中。
    若令牌无效或用户不存在，抛出 401 异常。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: int = payload.get("sub")  # 从 payload 中获取用户 ID（sub 字段）
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user


# 可选：获取当前活跃用户（增加 is_active 检查）
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user