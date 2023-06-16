import pytest
from sqlalchemy import insert, select

from auth.models import Role
from conftest import async_session_maker, client


async def test_create_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=0, name='user', permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        assert len(result.all()), 'Role was not added to database'


def test_register():
    response = client.post('/auth/register', json={
        'email': 'petya@mail.ru',
        'password': 'string',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'username': 'petya',
        'role_id': 0
    })

    assert response.status_code == 201


def test_login():
    response = client.post('/auth/login', data={'username': 'petya@mail.ru', 'password': 'string'})

    assert response.status_code == 204
