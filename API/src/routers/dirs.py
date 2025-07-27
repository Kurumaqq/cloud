from fastapi import APIRouter, Request
from src.schemas import *
from src import services

router = APIRouter(prefix='/dirs', tags=['dirs'])

@router.get('/list/{path:path}', response_model=ListDirsResponse)
async def list_dirs(path: str, request: Request) -> ListDirsResponse: 
    return await services.list_dirs(path, request)

@router.post('/create', response_model=CreateDirResponse)
async def create_dir(path: str, request: Request) -> CreateDirResponse:
    return await services.create_dir(path, request)

@router.post('/rename', response_model=RenameDirResponse)
async def rename_dir(path: str, new_name: str, request: Request) -> RenameDirResponse:
    return await services.rename_dir(path, new_name, request)

@router.post('/copy', response_model=CopyDirResponse)
async def copy_dir(dir_path: str, copy_path: str, request: Request):
    return await services.copy_dir(dir_path, copy_path, request)

@router.delete('/delete', response_model=DeleteDirResponse)
async def delete_dir(path: str, request: Request) -> DeleteDirResponse:    
   return await services.delete_dir(path, request)
