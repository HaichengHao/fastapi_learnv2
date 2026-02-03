# @Time    : 2026/1/28 10:43
# @Author  : hero
# @File    : routes.py
#important:pycharm批量替换ctrl+shift+alt+j
from typing import List

from alembic.util import status
from fastapi import APIRouter, Depends, HTTPException  # tips:使用依赖注入进行session的注入
from sqlmodel.ext.asyncio.session import AsyncSession
from  src.books.service import BookService
from src.books.schemas import Book, Book_update
from src.db.main import get_session
bookrt = APIRouter(prefix="/books", tags=["books"])

#important：实例化BookService对象
book_service = BookService()

@bookrt.get("/", response_model=List[Book])
async def get_all_books(session:AsyncSession=Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@bookrt.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: int,session:AsyncSession=Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@bookrt.post('/', response_model=Book)
async def create_a_book(book_data: Book,session:AsyncSession=Depends(get_session)):
    newbook = await book_service.create_a_book(book_data, session)
    return newbook

@bookrt.delete('/{book_uid}')
async def delete_a_book(book_uid: int,session:AsyncSession=Depends(get_session)):
    res = await book_service.delete_a_book(book_uid,session)
    if res:
        return res
    else:
        raise HTTPException(status_code=404,detail="Book not found")

@bookrt.patch('/{book_uid}', response_model=Book_update)
async def update_a_book(book_uid: int, book_data: Book_update, session:AsyncSession=Depends(get_session)):
    '''
    通过id来定位之后更新书籍
    :param id:
    :param book_data:
    :return: updated_bookdata
    '''
    update_book = await book_service.update_a_book(book_uid, book_data, session)
    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=404,detail="Book not found")

