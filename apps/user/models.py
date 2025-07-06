
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base
from utils import pwd_context

from apps.user.utils import utcnow


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

    @classmethod
    async def find_by_email(cls, db: AsyncSession, email: str):
        query = select(cls).where(cls.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def authenticate(cls, db: AsyncSession, email: str, password: str):
        user = await cls.find_by_email(db=db, email=email)
        if not user or not cls.verify_password(password, user.password):
            return False
        return user


class BlackListToken(Base):
    __tablename__ = "blacklisttokens"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    expire: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())