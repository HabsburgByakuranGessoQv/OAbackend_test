from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "OA System"
    debug: bool = False
    database_url: str = "mssql+pyodbc://sa:123456@localhost:1433/OAFastAPITest?driver=ODBC+Driver+17+for+SQL+Server"
    jwt_secret_key: str = "123456"
    secret_key: str = ""  # 添加这一行，可根据需要设置默认值
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "forbid"  # 或者改为 "ignore" 允许额外字段

settings = Settings()