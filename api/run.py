from fastapi import FastAPI
import uvicorn
from src.routers import master_router

app = FastAPI()
app.include_router(master_router)

# TODO: INHERIT FORM BASERESPONSE 
# TODO: FIX ERRORS
# TODO: EDIT FILENAME
# TODO: EDIT DIRNAME
# TODO: RESPONSE MODELS IN ROUTERS
# TODO: full_path_resolved to full_path

if __name__ == '__main__':
    uvicorn.run('run:app', reload=True)
