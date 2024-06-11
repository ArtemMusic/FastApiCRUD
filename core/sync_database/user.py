from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.sync_database.base import Base

if TYPE_CHECKING:
    from .email import EmailOrm


class UserORM(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    optional: Mapped[Optional[str]] = mapped_column(String(30))
    emails: Mapped[List['EmailOrm']] = relationship(back_populates='user', cascade="all, delete-orphan",
                                                      lazy='joined')
