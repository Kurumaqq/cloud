from fastapi import FastAPI
import uvicorn
from src.routers import dirs_router

app = FastAPI()
app.include_router(dirs_router)

if __name__ == '__main__':
    uvicorn.run('run:app', reload=True)
