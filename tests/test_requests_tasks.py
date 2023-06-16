from httpx import AsyncClient


async def test_add_task(ac: AsyncClient):
    response = await ac.post('/tasks', json={
        'title': 'test',
        'description': 'write tests on your app using pytest',
        'user_id': 1
    })

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json().get('status') == 'ok'
    assert response.json().get('data') == {}
    assert response.json().get('details') == {}


async def test_check_task(ac: AsyncClient):
    response = await ac.get('/tasks/1')

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json().get('status') == 'ok'
    assert response.json().get('data') != {}
    assert response.json().get('details') == {}


async def test_edit_task_status(ac: AsyncClient):
    response = await ac.put('/tasks', params={'task_id': 1})

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json().get('status') == 'ok'


async def test_delete_task(ac: AsyncClient):
    response = await ac.delete('/tasks', params={'task_id': 1})

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json().get('status') == 'ok'
    assert response.json().get('data') == {}
    assert response.json().get('details') == {}


# correct work of tests in this file needs to
# remove Depends(current_user) from all endpoints that are used in this file
# it means make all of them unprotected because login is made by cookies
# and executing request here will not have necessary cookies
# so every request to api here (from code) will get 401 response 'Unauthorized'
# if you will not remove Depends(current_user)