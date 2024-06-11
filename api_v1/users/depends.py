from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_v1.users.crud import engine
from api_v1.users.schemas import UserOut
from core.sync_database.user import UserORM


def get_user_by_id(user_id: int) -> Optional[UserOut]:
    with Session(engine) as session:
        user = session.query(UserORM).filter(UserORM.id == user_id).first()

        if user is not None:
            emails = [email.email for email in user.emails]
            return UserOut(
                id=user.id,
                name=user.name,
                emails=emails,
                optional=user.optional
            )

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
