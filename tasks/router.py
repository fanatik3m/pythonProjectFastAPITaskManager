from fastapi import APIRouter, Depends

from auth.users import current_user

router = APIRouter(
    prefix='/tasks',
    tags=['Task management'],
    dependencies=[Depends(current_user)]
)

