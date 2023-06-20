from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete, update

from sqlalchemy.ext.asyncio import AsyncSession

from auth.users import current_user
from auth.models import User
from database import get_async_session
from repository import Repository
from tasks.schemas import TaskCreate
from tasks.models import Task

router = APIRouter(
    prefix='/tasks',
    tags=['Task management']
)

db_repository = Repository()


@router.post('')
async def add_task(task: TaskCreate, session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    try:
        if task.user_id != user.id:
            task.user_id = user.id
        await db_repository.insert_user(session=session, data=task.dict())
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
        data = await db_repository.get_tasks_with_offset(session=session, page=page, user=user)
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
        data = await db_repository.get_task_by_id(session=session, task_id=task_id, user=user)
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
        data = await db_repository.get_ordered_tasks(session=session, date=date, is_completed=is_completed, user=user)
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
        await db_repository.delete_task(session=session, task_id=task_id, user=user)
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
        await db_repository.edit_status(session=session, task_id=task_id, user=user)
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
