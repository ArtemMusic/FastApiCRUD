from typing import Type

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from api_v1.users.schemas import UserCreateIn, UserUpdateIn
from core.sync_database.base import Base
from core.sync_database.user import UserORM

engine = create_engine("sqlite:///./sqliteSYNC.db", echo=True)
Base.metadata.create_all(engine)


def get_all_users() -> list[UserORM]:
    with Session(engine) as session:
        stmt = select(UserORM).order_by(UserORM.id.desc())
        return list(session.scalars(stmt))


def create_user(user: UserCreateIn) -> UserORM:
    with Session(engine) as session:
        data = user.model_dump()
        user = UserORM(**data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user(user):
    with Session(engine) as session:
        session.delete(user)
        session.commit()
        return user


def update_user(*, updated_user: UserUpdateIn, user: UserORM) -> UserORM | None:
    with Session(engine) as session:
        for key, value in updated_user.model_dump().items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
        return user
