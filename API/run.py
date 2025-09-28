from src.routers import master_router
from src.config import Config
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
config = Config()
origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
    "http://192.168.0.10:4173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(master_router)

if __name__ == '__main__':
    uvicorn.run(
        'run:app', 
        host=config.host,
        port=config.port,
        reload=True,
        )
