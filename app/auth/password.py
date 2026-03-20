from passlib.context import CryptContext

# 创建密码上下文，指定使用 bcrypt 算法（自动处理盐值）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    对明文密码进行哈希处理
    :param password: 明文密码
    :return: 哈希后的密码字符串
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码是否与哈希值匹配
    :param plain_password: 明文密码
    :param hashed_password: 哈希密码
    :return: 匹配返回 True，否则 False
    """
    return pwd_context.verify(plain_password, hashed_password)