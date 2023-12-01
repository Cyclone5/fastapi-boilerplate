from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select

from uuid import UUID, uuid4
from typing import Optional

from src.users.user.schemas import UserCreate, UserUpdate
from src.utils.single_psql_db import Base, get_db
from src.utils.exceptions import BadRequestError

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)

    @classmethod
    async def by_email(cls, email: str) -> "User":
        async with get_db() as db:
            stmt = select(cls).where(cls.email == email)
            return await db.scalar(stmt)

    @classmethod
    async def by_id(cls, user_id: UUID) -> "User":
        async with get_db() as db:
            stmt = select(cls).where(cls.id == user_id)
            return await db.scalar(stmt)

    @classmethod
    async def is_first_user(cls) -> bool:
        async with get_db() as db:
            stmt = select(cls)
            any_user = await db.scalar(stmt)
            if any_user is None:
                return True
            return False

    @classmethod
    async def create(cls, user: UserCreate) -> "User":
        async with get_db() as db:
            try:
                new_user = cls(**user.model_dump(exclude_none=True))
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)
                return new_user
            except (UniqueViolationError, IntegrityError) as e:
                raise BadRequestError("Kullanıcı oluşturulamadı. Bu e-posta adresi kullanılmaktadır.")

    @classmethod
    async def update(cls, user_id: UUID, data: UserUpdate) -> Optional["User"]:
        async with get_db() as db:
            user = await db.scalar(select(cls).where(cls.id == user_id))
            if user is None:
                return None
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(user, field, value)

            try:
                await db.commit()
                await db.refresh(user)
                return user
            except (UniqueViolationError, IntegrityError) as e:
                raise BadRequestError("Kullanıcı güncellenemedi. Bu e-posta adresi kullanılmaktadır.")

    @classmethod
    async def delete(cls, user_id: UUID) -> bool:
        async with get_db() as db:
            user = await db.scalar(select(cls).where(cls.id == user_id))
            if user is None:
                return None
            try:
                await db.delete(user)
                await db.commit()
                return user
            except (UniqueViolationError, IntegrityError):
                raise BadRequestError("Kullanıcı silinemedi. İletişime geçiniz.")
