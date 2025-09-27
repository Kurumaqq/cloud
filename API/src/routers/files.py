from fastapi import UploadFile, File, Request, Query, Response
from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import StreamingResponse, FileResponse
from src.schemas.files import *
from src.config import Config
from src import services

router = APIRouter(prefix='/files', tags=['files'])
config = Config()

@router.get('/download/{path:path}')
async def download_file(path: str, request: Request) -> DownloadFileErrorResponse:
    return await services.download_file(path, request)

@router.get('/list/{path:path}', response_model=ListFilesResponse)
async def list_files(path: str, request: Request) -> ListFilesResponse:
    return await services.list_files(path, request)

@router.get('/read/{path:path}', response_model=ReadFileResponse)
async def read_file(path: str, request: Request) -> ReadFileResponse:
    return await services.read_file(path, request)

@router.get('/get/{path:path}')
async def get_file(path: str, request: Request) -> StreamingResponse:
    return await services.get_file(path, request)

@router.post('/upload', response_model=UploadFileResponse)
async def upload_files(
    file: UploadFile = File(...),
    path: str = Query(""),
    request: Request = None
) -> UploadFileResponse:
    return await services.upload_file(file, path, request)


@router.post('/rename', response_model=RenameFileResponse)
async def rename_file(path: str, new_name: str, request: Request) -> RenameFileResponse:
    return await services.rename_file(path, new_name, request)

@router.post('/copy', response_model=CopyFileResponse)
async def copy_file(file_path: str, copy_path: str, request: Request) -> CopyFileResponse:
    return await services.copy_file(file_path, copy_path, request)

@router.delete('/delete', response_model=DeleteFilesResponse)
async def delete_file(path: str, request: Request) -> DeleteFilesResponse:
    return await services.delete_file(path, request)
