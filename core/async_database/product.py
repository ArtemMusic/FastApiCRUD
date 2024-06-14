from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.async_database.base import Base


class ProductORM(Base):
    __tablename__ = 'products'
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(60))
    price: Mapped[int] = mapped_column(Integer())
