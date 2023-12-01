from src.users.user.schemas import UserCreate, UserUpdate, UserMiniView
from src.users.user.models import User

from src.utils.single_psql_db import get_db
from src.utils.pagination import get_pagination_info
from src.utils.exceptions import NotFoundError, BadRequestError
from src.utils.schemas import GeneralResponse, PaginationGet, ListView

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
        # need_access(actor, ["*", "user.get"])
        async with get_db() as db:
            where_query = None
            if pagination_data.search:
                where_query = (
                        (User.first_name.like(f"%{pagination_data.search}%")) |
                        (User.last_name.like(f"%{pagination_data.search}%")) |
                        (User.email.like(f"%{pagination_data.search}%"))
                )
            if where_query is not None:
                query = select(User).where(where_query)
            else:
                query = select(User)
            if pagination_data.paginate:
                query = query.limit(pagination_data.pageSize).offset(
                    (pagination_data.page - 1) * pagination_data.pageSize
                )
            if pagination_data.order:
                query = query.order_by(User.updated_at.desc())

            users = await db.scalars(query)
            users = users.all()

            count = await User.get_count(where_query)
            pagination_info = get_pagination_info(total_items=count, current_page=pagination_data.page,
                                                  page_size=pagination_data.pageSize)

            return GeneralResponse(status=200, message="Users listed.",
                                   details=ListView[UserMiniView](info=pagination_info, items=users))

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
