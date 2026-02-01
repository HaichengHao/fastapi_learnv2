# @Time    : 2026/1/28 11:21
# @Author  : hero
# @File    : main.py

# important：创建引擎和session

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from config import Config
from src.books.models import Book #important:记住一定要显式导入
engine =   create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,  # 调试时打开，可以看到sql语句

)


# important:创建一个异步函数用于生命周期事件

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)  # tips:用同步的方式创建数据表
        # important:SQLModel.metadata.create_all将会扫描任何用这个SQLmodel对象创建并访问了元数据的模型
