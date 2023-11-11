from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.utils.schemas import PaginationGet
from src.auth.current_user import get_current_user
from src.users.user.models import User

from typing import Optional
from uuid import UUID

from src.users.user.schemas import UserCreate, UserUpdate
from src.users.user.service import UserService


users = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"SAGA-SOFT": "SAGA-SOFT"}},
)

@users.get("")
async def get_users(data: PaginationGet = Depends(),
                    current_user: User = Depends(get_current_user)):
    content = await UserService.get_users(pagination_data=data, actor=current_user)
    return JSONResponse(status_code=content.status, content=content.model_dump())

@users.get("/{user_id}")
async def get_user(user_id: UUID,
                   current_user: User = Depends(get_current_user)):
    content = await UserService.get_user(user_id=user_id, actor=current_user)
    return JSONResponse(status_code=content.status, content=content.model_dump())

@users.post("")
async def create_user(user: UserCreate,
                      current_user: User = Depends(get_current_user)):
    resp = await UserService.create(user=user, actor=current_user)
    return JSONResponse(status_code=resp.status, content=resp.model_dump())

@users.put("/{user_id}")
async def update_user(user_id: UUID, data: UserUpdate,
                      current_user: User = Depends(get_current_user)):
    resp = await UserService.update(user_id=user_id, data=data, actor=current_user)
    return JSONResponse(status_code=resp.status, content=resp.model_dump())

@users.delete("/{user_id}")
async def delete_user(user_id: UUID,
                      current_user: User = Depends(get_current_user)):
    resp = await UserService.delete(user_id=user_id, actor=current_user)
    return JSONResponse(status_code=resp.status, content=resp.model_dump())
