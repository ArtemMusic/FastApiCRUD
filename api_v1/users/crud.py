from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from api_v1.users.schemas import UserOut, UserIn
from core.sync_database.base import Base
from core.sync_database.user import UserORM
from core.sync_database.email import EmailOrm

engine = create_engine("sqlite:///./sqliteSYNC.db", echo=True)
Base.metadata.create_all(engine)


def get_all_users() -> Optional[List[UserOut]]:
    with Session(engine) as session:
        stmt = select(UserORM).order_by(UserORM.id.desc())
        users = session.scalars(stmt).unique()

        users_out = []
        for user in users:
            emails = [email.email for email in user.emails]
            user_out = UserOut(
                id=user.id,
                name=user.name,
                emails=emails,
                optional=user.optional
            )
            users_out.append(user_out)

    return users_out


def create_user(user) -> UserOut:
    with Session(engine) as session:
        data = user.model_dump()
        emails = data.pop('emails')

        check_valid_email(emails, session)

        user = UserORM(**data)
        user.emails = [EmailOrm(email=email) for email in emails]

        session.add(user)
        session.commit()
        session.refresh(user)

        return UserOut(
            id=user.id,
            name=user.name,
            emails=emails,
            optional=user.optional
        )


def delete_user(user_id) -> Optional[UserOut]:
    with Session(engine) as session:
        user = get_current_user(user_id, session)

        if user is not None:
            emails = [email.email for email in user.emails]
            user_data = UserOut(
                id=user.id,
                name=user.name,
                emails=emails,
                optional=user.optional
            )
            session.delete(user)
            session.commit()
            return user_data
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")


def update_user(*, updated_user: UserIn, user_id) -> UserOut:
    with Session(engine) as session:
        user = get_current_user(user_id, session)

        if user is not None:
            updated_user = updated_user.model_dump()
            for key, value in updated_user.items():
                if key == 'emails':
                    emails = value
                if key != 'emails':
                    setattr(user, key, value)

            updated_user.pop('emails')

            check_valid_email(emails, session)
            user.emails = [EmailOrm(email=email) for email in emails]

            session.commit()
            session.refresh(user)

            return UserOut(
                id=user.id,
                name=user.name,
                emails=emails,
                optional=user.optional
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")


def check_valid_email(emails, session) -> None:
    for email in emails:
        if "@" not in email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid email address: {email}")

        if session.query(EmailOrm).filter(EmailOrm.email.in_(emails)).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"{email} is already exist")


def get_current_user(user_id, session) -> UserORM:
    return session.query(UserORM).filter(UserORM.id == user_id).first()
