from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # 默认值 "bearer"