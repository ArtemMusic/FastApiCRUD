from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    description: str
    price: int


class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductOut(ProductBase):
    pass


class ProductIn(ProductBase):
    pass
