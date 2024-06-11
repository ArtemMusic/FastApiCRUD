from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.sync_database.base import Base

if TYPE_CHECKING:
    from .user import UserORM


class EmailOrm(Base):
    __tablename__ = 'emails'
    email: Mapped[str] = mapped_column(String(50), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserORM'] = relationship(back_populates='emails', lazy='joined')
