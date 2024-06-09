import uvicorn
from fastapi import FastAPI

from api_v1.users.views import router as user_router

app = FastAPI(
    title='CRUD'
)

app.include_router(prefix='/api/v1', router=user_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
