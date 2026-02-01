# @Time    : 2026/2/1 10:59
# @Author  : hero
# @File    : service.py
from fastapi import HTTPException
from sqlalchemy import Select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel, Book_update
from src.books.models import Book
from sqlmodel import select, desc, update


class BookService:
    async def get_all_books(self, session: AsyncSession):  # tips:利用依赖注入，构建异步Session
        # tips:还是跟sqlalchemy那时候学的一样有语句写法和非语句写法
        '''stmt = text("SELECT * FROM Book")
        books = await AsyncSession.exec(stmt).all()
        类原生sql写法
        '''

        # tips:按照创建时间降序排序,注意sqlalchemy和sqlmodel的写法略有不同
        # book_lst = await AsyncSession.exec(Select(Book).order_by(Book.created_at.desc())).all()

        # sqlmodel写法,能获得更好的代码提示哈哈
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement).all()
        return result

    async def get_book(self, book_uid: str, session: AsyncSession):
        stmt = select(Book).where(Book.uid == book_uid)
        result = await session.exec(stmt)
        book = result.first()
        return book if book is not None else None

    async def create_a_book(self, book_data: BookCreateModel, session: AsyncSession):
        # important:因为我们有schema,所以我们创建的时候可以采用mode_dump的操作

        new_book = Book(**book_data.model_dump())
        session.add(new_book)
        await session.commit()

        return new_book

    # async def update_a_book(self, book_uid: str, book_data: Book_update, session: AsyncSession):
    #     #tips:先进行查询看看书存不存在，存在了才能继续更新
    #     book_to_update = await self.get_book(book_uid, session)
    #     if book_to_update:
    #         stmt = update(Book).where(Book.uid == book_uid).values(book_data.model_dump(exclude_unset=True))
    #         await session.exec(stmt)
    #         await session.commit()
    #     else:
    #         raise HTTPException(status_code=400, detail="Book not found")
    async def update_a_book(self, book_uid: str, book_data: Book_update, session: AsyncSession):
        book = await self.get_book(book_uid, session)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # 只更新用户传的字段
        update_data = book_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)  # 动态赋值

        session.add(book)
        await session.commit()
        await session.refresh(book)  # 同步数据库最新状态（如 updated_at）
        return book

    async def delete_a_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return {
                'message': 'Book deleted successfully',
            }
