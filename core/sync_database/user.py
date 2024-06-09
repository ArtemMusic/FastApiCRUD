from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.sync_database.base import Base


class UserORM(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    optional: Mapped[str | None] = mapped_column(String(30))
