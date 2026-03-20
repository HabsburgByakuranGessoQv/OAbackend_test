import pyodbc

# 从 .env 中复制连接字符串（注意转义）
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01,1433;"
    "DATABASE=OASystem;"
    "UID=sa;"
    "PWD=123456"
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ 数据库连接成功！")
    conn.close()
except Exception as e:
    print("❌ 连接失败，错误信息：")
    print(e)
