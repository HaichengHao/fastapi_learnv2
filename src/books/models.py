# @Time    : 2026/1/28 13:34
# @Author  : hero
# @File    : models.py

from datetime import datetime, date
import sqlalchemy.dialects.postgresql  as pg
from sqlmodel import SQLModel,Field,Column #important:注意我们引入的Field不是Pydantic的那个！！
import uuid
class Book(SQLModel,table=True):
    __tablename__ = 'books'
    #设置id，自增
    #important:要使用sqlalchemy列类型或者特定的属性和东西,我们要做的就是访问`sa_column`属性
    uid:uuid.UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4()
        )
    )
    title:str=Field(nullable=False)
    author:str=Field(nullable=False)
    publisher:str
    page_count:int
    publish_date:date
    language:str
    created_at:datetime=Field(
         sa_column= Field(Column(pg.TIMESTAMP,default=datetime.now)) #important:也用到了psql特有的属性,所以也得是自定义列
    )
    updated_at:datetime=Field(
        sa_column=Field(Column(pg.TIMESTAMP,default=datetime.now))
    )


    #tips:这个是之前常用的
    # def __str__(self):
    #     return self.title
    #
    #tips:这次换一个
    def __repr__(self):
        return self.title
