from dataclasses import dataclass

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from tasks.models import Task


class Repository:
    async def insert_user(self, session: AsyncSession, data: dict):
        stmt = insert(Task).values(**data)
        await session.execute(stmt)
        await session.commit()

    async def get_tasks_with_offset(self, session: AsyncSession, page: int, user: User):
        offset = (page - 1) * 10
        query = select(Task).where(Task.user_id == user.id).order_by(Task.id).limit(10).offset(offset)
        result = await session.execute(query)
        data = result.scalars().all()
        return data

    async def get_task_by_id(self, session: AsyncSession, task_id: int, user: User):
        query = select(Task).where(Task.user_id == user.id).where(Task.id == task_id).order_by(Task.id).limit(10)
        result = await session.execute(query)
        data = result.scalars().all()
        return data

    async def get_ordered_tasks(self, session: AsyncSession, date: bool, is_completed: bool, user: User):
        if not date and not is_completed:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.id)
        if date and is_completed:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.id)

        if date:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.created_at)
        if is_completed:
            query = select(Task).where(Task.user_id == user.id).order_by(Task.is_completed)
        result = await session.execute(query)
        data = result.scalars().all()
        return data

    async def delete_task(self, session: AsyncSession, task_id: int, user: User):
        stmt = delete(Task).where(Task.id == task_id).where(Task.user_id == user.id)
        await session.execute(stmt)
        await session.commit()

    async def edit_status(self, session: AsyncSession, task_id: int, user: User):
        stmt = update(Task).where(Task.id == task_id).where(Task.user_id == user.id).values(is_completed=True)
        await session.execute(stmt)
        await session.commit()