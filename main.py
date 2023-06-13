from fastapi import FastAPI

from auth.schemas import UserRead, UserCreate
from auth.users import auth_backend, fastapi_users

from tasks.router import router as router_tasks

app = FastAPI(
    title='Task Manager'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_tasks)