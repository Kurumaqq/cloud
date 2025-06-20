from fastapi import APIRouter, UploadFile
from src.config import Config
from src.schemas.files import *
from src import services

router = APIRouter(prefix='/files', tags=['files'])
config = Config()

@router.get('/download/{path:path}')
async def download_file(path: str):
    return await services.download_file(path)

@router.get('/list/{path:path}', response_model=ListFilesResponse)
async def list_files(path: str):
    return await services.list_files(path)

@router.post('/upload', response_model=UploadFileResponse)
async def upload_files(file: UploadFile, path: str):
    return await services.upload_file(file, path)

@router.delete('/delete', response_model=DeleteFilesResponse)
async def delete_files(paths: list[str]):
    return await services.delete_files(paths)

@router.get('/read/{path:path}', response_model=ReadFileResponse)
async def read_file(path: str):
    return await services.read_file(path)

@router.post('/rename')
async def rename_file(path: str, new_name: str):
    return await services.rename_file(path, new_name)
