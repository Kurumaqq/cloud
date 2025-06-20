from fastapi.responses import FileResponse
from fastapi import UploadFile
from src.errors.files import *
from pathlib import Path
from src.config import Config
from src.schemas.files import *
from src.utils import check_path
from src.errors.dirs import NotDirHttpError

config = Config()

async def list_files(path):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)

        if not full_path.exists() or not full_path.is_dir():
            raise FileNotFoundError(f'Directory {path} does not exist.')

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
   

async def download_file(path: str):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)   

        if not full_path.exists() or not full_path.is_file():
            raise FileNotFoundError(f'File {path} does not exist.')

        return FileResponse(
            path=str(full_path),
            media_type='application/octet-stream',
            filename=path.split('/')[-1] 
        )
    except Exception as e:
        return DownloadFileErrorResponse(
            status='error',
            message=str(e)
        )

async def delete_files(paths: list[str]): 
    try: 
        for path in paths:
            check_path(path)
        full_paths_resolved = [
            (Path(config.base_dir) / path).resolve() 
            for path in paths
        ]
        
        for path in full_paths_resolved:
            if not path.exists(): raise FileNotFoundHttpError(path)
            if not path.is_file(): raise NotFileHttpError(path)
            path.unlink()

        return DeleteFilesResponse(
            status='ok',
            message=f'Files {paths} deleted successfully.'
        )
    except Exception as e:
        return DeleteFilesResponse(
            status='error',
            message=str(e)
        )


async def upload_file(file: UploadFile, path: str):
    try: 
        filename = file.filename
        full_path = (Path(config.base_dir) / path / filename).resolve()
        check_path(path)
        check_path(filename)

        if full_path.exists():
            raise FileExistsHttpError(path)
        if full_path.is_dir():
            raise NotDirHttpError(path)

        with open(str(full_path), 'wb') as f:
            while content := await file.read(30 * 1024 * 1024):  
                f.write(content)

        if not path or path.strip() == '': path = '/'

        return UploadFileResponse(
            status='ok',
            message=f'File {filename} uploaded successfully to {path}.'
        )

    except Exception as e: 
        return UploadFileResponse(
            status='error',
            message=str(e)
        )   
async def read_file(path: str):
    try:
        data = ''
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)
        if not full_path.exists():
            raise FileNotFoundHttpError(path)
        if not full_path.is_file():
            raise NotFileHttpError(path)

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
