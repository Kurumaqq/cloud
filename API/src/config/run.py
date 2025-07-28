from src.routers import master_router
from src.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
config = Config()
app.include_router(master_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(
        'run:app', 
        host=config.host,
        port=config.port,
        reload=True
        )
