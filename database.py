from fastapi import HTTPException, status
from pydantic import PostgresDsn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from config import get_settings

PG_URL = str(
    PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username=get_settings().postgres_user,
        password=get_settings().postgres_password,
        host=get_settings().postgres_host,
        port=get_settings().postgres_port,
        path=f"{get_settings().postgres_db}",
    )
)


engine = create_async_engine(PG_URL, future=True, echo=True)


SessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        await db.close()


class Base(AsyncAttrs, DeclarativeBase):
    async def save(self, db: AsyncSession):
        """
        :param db:
        :return:
        """
        try:
            db.add(self)
            return await db.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex
        
    async def delete(self, db: AsyncSession):
        """
        :param db:
        :return:
        """
        try:
            await db.delete(self)
            return await db.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex
    @classmethod
    async def find_by_id(cls, db: AsyncSession, id: any):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalars().first()