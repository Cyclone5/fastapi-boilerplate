from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.auth.base.schemas import LoginSchema, RegisterSchema
from src.users.user.models import User
from src.users.user.schemas import UserMeView
from src.auth.base.service import AuthService
from src.auth.current_user import get_current_user

from src.settings import config

auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"SAGA-SOFT": "SAGA-SOFT"}},
)


@auth.post("/sign-in")
async def login(loginSchema: LoginSchema):
    content = await AuthService.login(loginSchema)
    resp = JSONResponse(status_code=content.status, content=content.model_dump())
    resp.set_cookie("Authorization", value=content.details, max_age=60*config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return resp

@auth.post("/sign-up")
async def register(registerSchema: RegisterSchema):
    content = await AuthService.register(registerSchema)
    resp = JSONResponse(status_code=content.status, content=content.model_dump())
    resp.set_cookie("Authorization", value=content.details, max_age=60*config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return resp

@auth.post("/sign-out")
async def logout():
    resp = JSONResponse(status_code=200, content={"message": "Başarıyla Çıkış Yapıldı."})
    resp.delete_cookie("Authorization")
    return resp

@auth.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return JSONResponse(status_code=200, content=UserMeView.model_validate(current_user).model_dump())

@auth.post("/forgot-password")
async def forgot_password():
    pass

@auth.post("/reset-password")
async def reset_password():
    pass

@auth.post("/oauth2/google")
async def google_login():
    pass
