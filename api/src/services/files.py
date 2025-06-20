from src.utils import check_path, check_file, check_paths, check_token
from fastapi.responses import FileResponse
from src.errors.dirs import NotDirHttpError
from fastapi import UploadFile, Request
from src.schemas.files import *
from src.errors.files import *
from src.config import Config
from pathlib import Path

config = Config()

async def list_files(path: str, request: Request):
    try:
        token = request.headers['Authorization']
        full_path = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)

        if not full_path.is_dir():
            raise NotDirHttpError(path)

        files = [
            str(f.as_posix()) 
            for f in full_path.iterdir() 
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
   

async def download_file(path: str, request: Request):
    try:
        token = request.headers['Authorization']
        full_path = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)   
        check_file(full_path)

        return FileResponse(
            path=str(full_path),
            media_type='application/octet-stream',
            filename=full_path.name
        )
    except Exception as e:
        return DownloadFileErrorResponse(
            status='error',
            message=str(e)
        )

async def delete_files(paths: list[str], request: Request): 
    try: 
        full_path = [(Path(config.base_dir) / path).resolve() for path in paths]
        token = request.headers['Authorization']
        
        check_token(token)
        check_paths(paths)

        for path in full_path:
            check_file(path)
            path.unlink()

        return DeleteFilesResponse(
            status='ok',
            files=paths,
            message=f'Files {paths} deleted successfully.'
        )
    except Exception as e:
        return DeleteFilesResponse(
            status='error',
            files=paths,
            message=str(e)
        )


async def upload_file(file: UploadFile, path: str, request: Request):
    try: 
        filename = file.filename
        full_path = (Path(config.base_dir) / path / filename).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_paths([path, filename])

        with open(str(full_path), 'wb') as f:
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
async def read_file(path: str, request: Request):
    try:
        data = ''
        full_path = (Path(config.base_dir) / path).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_path(path)
        check_file(full_path)

        with open(full_path, 'r') as f: data = f.read()

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

async def rename_file(path: str, new_name: str, request: Request):
    try:
        old_name = Path(path).name
        old_ext = Path(old_name).suffix
        if new_name.count('.') == 0: new_name += old_ext
        
        full_path = (Path(config.base_dir) / path).resolve()
        new_path = (Path(config.base_dir) / new_name).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_paths([path, new_name])
        check_file(full_path)

        full_path.rename(new_path)

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
