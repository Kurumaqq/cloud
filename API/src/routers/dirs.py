from fastapi import APIRouter, Request, Response
from src.schemas import *
from src import services

router = APIRouter(prefix='/dirs', tags=['dirs'])

@router.get('/list/{path:path}', response_model=ListDirsResponse)
async def list_dirs(path: str, request: Request, response: Response) -> ListDirsResponse: 
    return await services.list_dirs(path, request, response)

@router.get('/size/{path:path}', response_model=SizeDirResponse)
async def size_dir(path: str, request: Request, response: Response) -> SizeDirResponse:
    return await services.size_dir(path, request, response)

@router.post('/create', response_model=CreateDirResponse)
async def create_dir(path: str, request: Request, response: Response) -> CreateDirResponse:
    return await services.create_dir(path, request, response)

@router.post('/rename', response_model=RenameDirResponse)
async def rename_dir(path: str, new_name: str, request: Request, response: Response) -> RenameDirResponse:
    return await services.rename_dir(path, new_name, request, response)

@router.post('/copy', response_model=CopyDirResponse)
async def copy_dir(dir_path: str, copy_path: str, request: Request, response: Response):
    return await services.copy_dir(dir_path, copy_path, request, response)

@router.delete('/delete', response_model=DeleteDirResponse)
async def delete_dir(path: str, request: Request, response: Response) -> DeleteDirResponse:    
   return await services.delete_dir(path, request, response)
