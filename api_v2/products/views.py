from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v2.products import crud
from api_v2.products.schemas import ProductOut, Product, ProductIn
from core.async_database.depends import get_product_by_id, session_depends

router = APIRouter(
    prefix='/product', tags=['products [async]']
)


@router.post('/create', response_model=ProductOut)
async def create_product(product: ProductIn, session: AsyncSession = session_depends) -> ProductOut:
    return await crud.create_product(product, session)


@router.get('/all', response_model=List[Product])
async def get_all_products(session: AsyncSession = session_depends) -> List[Product]:
    return await crud.get_all_products(session)


@router.get('/{product_id}', response_model=Product)
async def get_product_by_id(product=Depends(get_product_by_id)) -> Product:
    return product


@router.delete('/{product_id}', response_model=Product)
async def delete_product(product_id: int, session: AsyncSession = session_depends) -> Product:
    return await crud.delete_product(product_id, session)


@router.put('/{product_id}/update', response_model=Product)
async def update_product(updated_product: ProductIn, product_id, session: AsyncSession = session_depends) -> Product:
    return await crud.update_product(updated_product, product_id, session)
