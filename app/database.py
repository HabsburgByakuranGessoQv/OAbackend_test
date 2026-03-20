from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings  # 从配置文件中读取数据库连接信息

# 从配置中获取数据库 URL（例如 "mssql+pyodbc://sa:password@localhost:1433/OA?driver=ODBC+Driver+17+for+SQL+Server"）
SQLALCHEMY_DATABASE_URL = settings.database_url

# 创建数据库引擎
# pool_pre_ping=True 用于检查连接是否有效，避免使用已断开的连接，对 SQL Server 很有用
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    # 如果需要 echo 日志，可以添加 echo=True，生产环境不建议开启
)

# 创建 SessionLocal 类，每个实例代表一个数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 基类，所有 ORM 模型都需要继承它
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    """
    每个请求调用一次，生成一个数据库会话，请求结束后关闭。
    用于 FastAPI 的依赖注入系统。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()