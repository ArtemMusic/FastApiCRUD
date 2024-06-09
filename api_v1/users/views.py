from fastapi import APIRouter, Depends

from api_v1.users import crud
from api_v1.users.depends import get_user_by_id
from api_v1.users.schemas import UserCreateOut, UserOut, UserDeleteOut, UserCreateIn, UserUpdateIn
from core.sync_database.user import UserORM

router = APIRouter(
    prefix='/user', tags=['users']
)


@router.get('/all', response_model=list[UserOut])
def get_all_users() -> list[UserORM]:
    return crud.get_all_users()


@router.get('/{user_id}', response_model=UserOut | None)
def get_user_by_id(user: UserORM = Depends(get_user_by_id)) -> UserORM | None:
    return user


@router.post('/create', response_model=UserCreateOut)
def create_user(user: UserCreateIn) -> UserORM:
    return crud.create_user(user)


@router.delete('/{user_id}', response_model=UserDeleteOut | None)
def delete_user_by_id(user: UserORM = Depends(get_user_by_id)) -> UserORM | None:
    return crud.delete_user(user)


@router.put('/{user_id}/update', response_model=UserDeleteOut | None)
def update_user(updated_user: UserUpdateIn, user: UserORM = Depends(get_user_by_id)):
    return crud.update_user(updated_user=updated_user, user=user)
