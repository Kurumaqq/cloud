from fastapi import FastAPI
import uvicorn
from src.routers import master_router

app = FastAPI()
app.include_router(master_router)

# TODO: EDIT FILENAME
# TODO: EDIT DIRNAME

if __name__ == '__main__':
    uvicorn.run('run:app', reload=True)
