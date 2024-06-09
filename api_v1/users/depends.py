from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_v1.users.crud import engine
from core.sync_database.user import UserORM


def get_user_by_id(user_id: int) -> Type[UserORM]:
    with Session(engine) as session:
        user = session.get(UserORM, {'id': user_id})

        if user is not None:
            return user

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
