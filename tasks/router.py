from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete, update

from sqlalchemy.ext.asyncio import AsyncSession

from auth.users import current_user
from auth.models import User
from database import get_async_session
from tasks.schemas import TaskCreate
from tasks.models import Task

router = APIRouter(
    prefix='/tasks',
    tags=['Task management']
)


@router.post('')
async def add_task(task: TaskCreate, session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    try:
        if task.user_id != user.id:
            task.user_id = user.id
        stmt = insert(Task).values(**task.dict())
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


@router.get('')
async def check_tasks(page: int = 1, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    try:
        offset = (page - 1) * 10
        query = select(Task).where(Task.user_id == user.id).order_by(Task.id).limit(10).offset(offset)
        result = await session.scalars(query)
        data = [row for row in result]
        return {
            'status': 'ok',
            'details': {},
            'data': data
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'details': {'message': str(ex)},
            'data': {}
        })


@router.get('/{task_id}')
async def check_tasks(task_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    try:
        query = select(Task).where(Task.user_id == user.id).where(Task.id == task_id).order_by(Task.id).limit(10)
        result = await session.scalars(query)
        data = [row for row in result]
        return {
            'status': 'ok',
            'details': {},
            'data': data
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'details': {'message': str(ex)},
            'data': {}
        })


@router.get('/ordered_tasks')
async def filter_tasks(date: bool = False, is_completed: bool = False,
                       session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    try:
        if not date and not is_completed:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.id)
        if date and is_completed:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.id)

        if date:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.created_at)
        if is_completed:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.is_completed)
        result = await session.scalars(query)
        data = [row for row in result]
        return {
            'status': 'ok',
            'details': {},
            'data': data
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'details': {'message': str(ex)},
            'data': {}
        })


@router.delete('')
async def delete_tasks(task_id: int, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        stmt = delete(Task).where(Task.id == task_id).where(Task.user_id == user.id)
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


@router.put('')
async def mark_as_completed(task_id: int, session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user)):
    try:
        stmt = update(Task).where(Task.id == task_id).where(Task.user_id == user.id).values(is_completed=True)
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'ok',
            'detail': {},
            'data': {}
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'details': {'message': str(ex)},
            'data': {}
        })
