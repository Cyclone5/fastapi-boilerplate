from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.utils.single_psql_db import init_psql_db
from src.utils.exceptions import GeneralException

from src.auth.base.router import auth
from src.users.user.router import users

app = FastAPI()

app.include_router(auth)
app.include_router(users)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_psql_db()

@app.exception_handler(GeneralException)
async def general_exception_handler(request: Request, exc: GeneralException):
    return JSONResponse(status_code=exc.general_response.status, content=exc.general_response.model_dump(),
                        headers=exc.headers)
