from src.routers import master_router
from src.config import Config
from fastapi import FastAPI
import uvicorn

app = FastAPI()
config = Config()
app.include_router(master_router)

if __name__ == '__main__':
    uvicorn.run(
        'run:app', 
        host=config.host,
        port=config.port,
        )
