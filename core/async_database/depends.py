from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v2.products.schemas import Product
from core.async_database.database import database
from core.async_database.product import ProductORM

session_depends = Depends(database.scoped_session_dependency)


async def get_product_by_id(product_id: int, session: AsyncSession = session_depends) -> Product:
    stmt = select(ProductORM).where(ProductORM.id == product_id)
    product = await session.scalar(stmt)

    if product is not None:
        return Product(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
