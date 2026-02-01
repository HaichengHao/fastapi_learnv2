# @Time    : 2026/1/28 10:42
# @Author  : hero
# @File    : __init__.py.py

from fastapi import FastAPI
from src.books.routes import bookrt

# important:创建生命周期事件
from contextlib import asynccontextmanager  # important:一旦创建将会定义哪些代码在启动时运行，哪些在结束时运行

from src.db.main import init_db

@asynccontextmanager
async def life_sapn(app: FastAPI):
    print('服务器正在启动')
    #important:在服务启动时链接数据库
    await init_db() #tips:注意initdb是一个异步函数,所以需要await调用

    yield
    print('服务器已经停止')


version = 'v1'

app = FastAPI(
    title='书籍存储仓后端api',
    description='用于书籍仓储服务的版本',
    version=version,
    lifespan=life_sapn #important:给它指明生命周期
)
app.include_router(bookrt, prefix=f'/api/{version}')
