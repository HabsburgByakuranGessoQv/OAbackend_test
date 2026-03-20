from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from jose import JWTError, jwt
from app.config import settings  # 导入配置


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    生成 JWT 访问令牌
    :param data: 要编码到 token 中的 payload 数据（如 {"sub": user_id, "username": ...}）
    :param expires_delta: 可选的自定义过期时间，若不提供则使用配置中的默认值
    :return: 编码后的 JWT 字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    解码并验证 JWT 令牌
    :param token: JWT 字符串
    :return: 解码后的 payload 字典
    :raises JWTError: 如果令牌无效或已过期
    """
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    return payload