import asyncio
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v2.products.schemas import ProductOut, Product, ProductIn
from core.async_database.base import Base
from core.async_database.database import database
from core.async_database.product import ProductORM


async def create_database():
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


asyncio.run(create_database())


async def create_product(product: ProductIn, session: AsyncSession) -> ProductOut:
    data = product.model_dump()
    product = ProductORM(**data)
    session.add(product)

    product = ProductOut(
        title=product.title,
        description=product.description,
        price=product.price
    )

    await session.commit()
    return product


async def get_all_products(session: AsyncSession) -> List[Product]:
    stmt = select(ProductORM).order_by(ProductORM.id.desc())
    result: Result = await session.execute(stmt)
    products = list(result.scalars())

    products_out = []
    for product in products:
        products_out.append(
            Product(
                id=product.id,
                title=product.title,
                description=product.description,
                price=product.price
            )
        )

    return products_out


async def delete_product(product_id: int, session: AsyncSession) -> Product:
    stmt = select(ProductORM).where(ProductORM.id == product_id)
    result: Result = await session.execute(stmt)
    product = result.scalar()

    if product is not None:
        await session.delete(product)
        await session.commit()

        return Product(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")


async def update_product(updated_product: ProductIn, product_id: int, session: AsyncSession) -> Product:
    stmt = select(ProductORM).where(ProductORM.id == product_id)
    result: Result = await session.execute(stmt)
    product = result.scalar()

    if product is not None:
        updated_product = updated_product.model_dump()

        for key, value in updated_product.items():
            setattr(product, key, value)

        product = Product(
            id = product.id,
            title=product.title,
            description=product.description,
            price=product.price
        )

        await session.commit()
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
