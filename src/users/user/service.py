from src.users.user.schemas import UserCreate, UserUpdate
from src.users.user.models import User

from src.utils.single_psql_db import get_db
from src.utils.pagination import get_pagination_info
from src.utils.exceptions import NotFoundError, BadRequestError
from src.utils.schemas import GeneralResponse, PaginationGet

from src.auth.access.service import has_access, need_access

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Union
from uuid import UUID
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError

class UserService:

    @staticmethod
    async def create(user: UserCreate, actor: User):
        need_access(actor, ["*", "user.create"])
        await User.create(user)
        return GeneralResponse(status=201, message="User created successfully.")

    @staticmethod
    async def get_users(pagination_data: PaginationGet, actor: User):
        need_access(actor, ["*", "user.get"])
        pass
        # @TODO

    @staticmethod
    async def get_user(user_id: UUID, actor: User):
        need_access(actor, ["*", "user.get"])
        user = await User.by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        return GeneralResponse(status=200, message="User found.", data=user)

    @staticmethod
    async def update(user_id: UUID, data: UserUpdate, actor: User):
        need_access(actor, ["*", "user.update"])
        await User.update(user_id, data)
        return GeneralResponse(status=200, message="User updated successfully.")

    @staticmethod
    async def delete(user_id: UUID, actor: User):
        need_access(actor, ["*", "user.delete"])
        await User.delete(user_id)
        return GeneralResponse(status=200, message="User deleted successfully.")
