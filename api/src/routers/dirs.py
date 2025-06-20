from fastapi import APIRouter
from src import services
from src.schemas import *

router = APIRouter(prefix='/dirs', tags=['dirs'])

@router.get('/list/{path:path}', response_model=ListDirsResponse)
async def list_dirs(path: str): 
    return await services.list_dirs(path)

@router.post('/create', response_model=CreateDirResponse)
async def create_dir(path: str):
    return await services.create_dir(path)

@router.delete('/delete', response_model=DeleteDirResponse)
async def delete_dir(path: str):    
   return await services.delete_dir(path)
