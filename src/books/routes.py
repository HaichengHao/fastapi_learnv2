# @Time    : 2026/1/28 10:43
# @Author  : hero
# @File    : routes.py
#important:pycharm批量替换ctrl+shift+alt+j
from typing import List
from fastapi import APIRouter
from src.books.schemas import Book, Book_update

bookrt = APIRouter(prefix="/books", tags=["books"])


@bookrt.get("/", response_model=List[Book])
async def get_all_books() -> List[dict]:
    pass


@bookrt.get("/{id}", response_model=Book)
async def get_book(book_id: int) -> dict:
    pass


@bookrt.post('/', response_model=Book)
async def create_a_book(book_data: Book):
    new_book = book_data.model_dump()  # tips:将json转换为字典格式方便之后直接利用创建模型对象的方式存储
    pass


@bookrt.delete('/{id}')
async def delete_a_book(id: int):
    pass


@bookrt.patch('/{id}', response_model=Book_update)
async def update_a_book(id: int, book_data: Book, ):
    '''
    通过id来定位之后更新书籍
    :param id:
    :param book_data:
    :return: updated_bookdata
    '''
    pass
