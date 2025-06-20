from fastapi import APIRouter, UploadFile
from src.config import Config
from src.schemas import *
from src import services

router = APIRouter(prefix='/files', tags=['files'])
config = Config()

#TODO: RESPONSE MODELS
@router.get('/download/{path:path}')
async def download_file(path: str):
    return await services.download_file(path)

@router.get('/list/{path:path}')
async def list_files(path: str):
    return await services.list_files(path)

@router.post('/upload')
async def upload_files(file: UploadFile, path: str):
    return await services.upload_file(file, path)

@router.delete('/delete')
async def delete_files(paths: list[str]):
    return await services.delete_files(paths)

@router.get('/read/{path:path}')
async def read_file(path: str):
    return await services.read_file(path)
