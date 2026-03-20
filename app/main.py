from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, departments
from app.database import engine, Base, SessionLocal
from app import models  # 确保所有模型被导入

app = FastAPI(title="OA System API", version="1.0.0")

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(departments.router)

@app.on_event("startup")
def init_db():
    # 开发环境创建表
    Base.metadata.create_all(bind=engine)
    init_default_roles()

def init_default_roles():
    db = SessionLocal()
    # 检查 employee 角色是否存在
    emp_role = db.query(models.Role).filter_by(name="employee").first()
    if not emp_role:
        emp_role = models.Role(name="employee", description="Regular employee")
        db.add(emp_role)
    # 还可以添加 admin 角色等
    admin_role = db.query(models.Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = models.Role(name="admin", description="Administrator")
        db.add(admin_role)
    db.commit()
    db.close()

@app.get("/")
def root():
    return {"message": "OA System API Running"}
