import uvicorn
from fastapi import FastAPI

from api_v1.users.views import router as user_router
from api_v2.products.views import router as product_router

app = FastAPI(
    title='CRUD'
)

app.include_router(prefix='/api/v1', router=user_router)
app.include_router(prefix='/api/v2', router=product_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
