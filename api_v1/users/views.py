from typing import List, Optional

from fastapi import APIRouter, Depends

from api_v1.users import crud
from api_v1.users.depends import get_user_by_id
from api_v1.users.schemas import UserOut, UserIn

router = APIRouter(
    prefix='/user', tags=['users']
)


@router.get('/all', response_model=Optional[List[UserOut]])
def get_all_users() -> Optional[List[UserOut]]:
    return crud.get_all_users()


@router.get('/{user_id}', response_model=Optional[UserOut])
def get_user_by_id(user: UserOut = Depends(get_user_by_id)) -> Optional[UserOut]:
    return user


@router.post('/create', response_model=UserOut)
def create_user(user: UserIn) -> UserOut:
    return crud.create_user(user)


@router.delete('/{user_id}', response_model=Optional[UserOut])
def delete_user_by_id(user_id: int) -> Optional[UserOut]:
    return crud.delete_user(user_id)


@router.put('/{user_id}/update', response_model=UserOut)
def update_user(updated_user: UserIn, user_id: int) -> UserOut:
    return crud.update_user(updated_user=updated_user, user_id=user_id)
