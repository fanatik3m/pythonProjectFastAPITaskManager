from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import Role
from auth.schemas import UserRead, UserCreate
from auth.users import auth_backend, fastapi_users
from database import get_async_session
from add_role_schema import AddRoleSchema

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


@app.post('/role/add')
async def add_role(data: AddRoleSchema, session: AsyncSession = Depends(get_async_session)):
    try:
        password: str = 'admin_admin_only_password545332ksajdKJHDJKSAhdjaskdsladkasdJdKASKS'
        if data.password != password:
            raise HTTPException(status_code=403, detail={
                'status': 'error',
                'details': {'message': 'Forbidden'},
                'data': {'admin_password': 'incorrect'}
            })

        stmt = insert(Role).values(id=data.id, name=data.name)
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'ok',
            'details': {},
            'data': {}
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'details': {'message': str(ex)},
            'data': {}
        })
