from src.utils import check_path, check_file, check_paths, check_token, chunk_generator, unique_name, copy_file_thread
from fastapi.responses import FileResponse, StreamingResponse
from src.errors.dirs import NotDirHttpError
from fastapi import UploadFile, Request
from mimetypes import guess_type
from src.schemas.files import *
from src.errors.files import *
from src.config import Config
from pathlib import Path
import asyncio
import shutil
import os

config = Config()

async def list_files(path: str, request: Request) -> ListFilesResponse:
    try:
        token = request.headers['Authorization']
        src_dir = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)

        if not src_dir.is_dir():
            raise NotDirHttpError(path)

        files = [
            str(f.as_posix()) 
            for f in src_dir.iterdir() 
            if f.is_file()
            ]
        
        return ListFilesResponse(
            status='ok',
            files=files,
            message='Files listed successfully.'
        )
    except Exception as e:
        return ListFilesResponse(
            status='error',
            message=str(e)
        )
   

async def download_file(path: str, request: Request) -> FileResponse | DownloadFileErrorResponse:
    try:
        token = request.headers['Authorization']
        src_dir = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)   
        check_file(src_dir)

        return FileResponse(
            path=str(src_dir),
            media_type='application/octet-stream',
            filename=src_dir.name
        )
    except Exception as e:
        return DownloadFileErrorResponse(
            status='error',
            message=str(e)
        )

async def delete_file(path: str, request: Request) -> DeleteFilesResponse: 
    try: 
        src_dir = (Path((config.base_dir)) / path).resolve()
        token = request.headers['Authorization']
        
        check_token(token)
        check_path(path)
        check_file(src_dir)

        src_dir.unlink()

        return DeleteFilesResponse(
            status='ok',
            files=path,
            message=f'File {path} deleted successfully.'
        )
    except Exception as e:
        return DeleteFilesResponse(
            status='error',
            files=path,
            message=str(e)
        )


async def upload_file(file: UploadFile, path: str, request: Request) -> UploadFileResponse:
    try: 
        filename = file.filename
        src_dir = (Path(config.base_dir) / path / filename).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_paths([path, filename])

        with open(str(src_dir), 'wb') as f:
            while content := await file.read(30 * 1024 * 1024):  
                f.write(content)

        if not path or path.strip() == '': path = '/'

        return UploadFileResponse(
            status='ok',
            filename=filename,
            message=f'File {filename} uploaded successfully to {path}.'
        )

    except Exception as e: 
        return UploadFileResponse(
            status='error',
            filename=filename,
            message=str(e)
        )   
async def read_file(path: str, request: Request) -> ReadFileResponse:
    try:
        data = ''
        src_dir = (Path(config.base_dir) / path).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_path(path)
        check_file(src_dir)

        with open(src_dir, 'r') as f: data = f.read()

        return ReadFileResponse(
            status='ok',
            content=data,
            message=f'File {path} read successfully.'
        )
    except Exception as e: 
        return ReadFileResponse(
            status='error',
            message=str(e)
        )
    
async def rename_file(path: str, new_name: str, request: Request) -> RenameFileResponse:
    try:
        old_name = Path(path).name
        old_ext = Path(old_name).suffix
        if new_name.count('.') == 0: new_name += old_ext
        
        src_dir = (Path(config.base_dir) / path).resolve()
        new_path = (Path(config.base_dir) / new_name).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_paths([path, new_name])
        check_file(src_dir)

        src_dir.rename(new_path)

        return RenameFileResponse(
            status='ok',
            old_name=old_name,
            new_name=new_name,
            message=f'File {old_name} renamed to {new_name} successfully.'
        )
    except Exception as e: 
        return RenameFileResponse(
            status='error',
            old_name=old_name,
            new_name=new_name,
            message=str(e)
        )

async def copy_file(file_path: str, copy_path: str, request: Request) -> CopyFileResponse:
    try:
        token = request.headers['Authorization']
        src_file = (Path(config.base_dir) / file_path).resolve()
        dst_file = (Path(config.base_dir) / copy_path).resolve()
        check_token(token)
        check_paths([file_path, copy_path])
        check_file(src_file)

        file_name = src_file.name
        target_path = unique_name(dst_file, file_name, 'file')
        name = target_path.name

        await copy_file_thread(src_file, target_path)
        return CopyFileResponse(
            status='ok',
            old_path=file_path,
            new_path=copy_path,
            name=name,
            message=f'Directory {file_path} copy to {copy_path} successfully.'
        )
    except Exception as e: 
        return CopyFileResponse(
            status='error',
            old_path=file_path,
            new_path=copy_path,
            message=str(e)
        )

async def get_file(path: str, request: Request):
    try:
        filename = path.split('/')[-1]
        src_dir = (Path(config.base_dir) / path).resolve()
        token = request.headers['Authorization']
        check_token(token)
        check_path(path)  

        mime_type = guess_type(filename)[0] or "application/octet-stream"
        file_size = os.path.getsize(src_dir)
        chunk_size = 5 * 1024 * 1024 
        
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
        }
        return StreamingResponse(
            chunk_generator(src_dir, chunk_size),
            headers=headers,
            media_type=mime_type,
        )
    except Exception as e:
        return GetFileErrorResponse(
            status='error',
            filename=filename,
            message=str(e)
        ) 
