from fastapi import APIRouter, UploadFile
from src.schemas.files import *
from src.config import Config
from src import services

router = APIRouter(prefix='/files', tags=['files'])
config = Config()

@router.get('/download/{path:path}')
async def download_file(path: str, request):
    return await services.download_file(path, request)

@router.get('/list/{path:path}', response_model=ListFilesResponse)
async def list_files(path: str, request):
    return await services.list_files(path, request)

@router.get('/read/{path:path}', response_model=ReadFileResponse)
async def read_file(path: str, request):
    return await services.read_file(path, request)

@router.post('/upload', response_model=UploadFileResponse)
async def upload_files(file: UploadFile, path: str, request):
    return await services.upload_file(file, path, request)

@router.post('/rename')
async def rename_file(path: str, new_name: str, request):
    return await services.rename_file(path, new_name, request)

@router.delete('/delete', response_model=DeleteFilesResponse)
async def delete_files(paths: list[str], request):
    return await services.delete_files(paths, request)
