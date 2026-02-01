# @Time    : 2026/1/28 10:40
# @Author  : hero
# @File    : schemas.py
from pydantic import BaseModel
import uuid
from datetime import datetime


# 创建schema
class Book(BaseModel):
    uid: uuid.UUID  # tips:对应service中的类型
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    page_count: int
    publish_date: str


class Book_update(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
