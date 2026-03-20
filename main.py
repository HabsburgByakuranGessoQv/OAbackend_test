from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
async def root():
    # return {"message": "Hello World"}
    return {"message": "测试成功，服务器正在运行并监听"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": f"Hello {name}, Time is {time_now}"}
