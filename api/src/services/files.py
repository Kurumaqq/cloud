from fastapi.responses import FileResponse
from fastapi import UploadFile
from src.errors.files import *
from pathlib import Path
from src.config import Config
from src.schemas.files import *
from src.utils import check_path, check_file, check_paths
from src.errors.dirs import NotDirHttpError

config = Config()

async def list_files(path):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
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
   

async def download_file(path: str):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)   
        check_file(full_path)

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
        check_paths(paths)

        full_path = [
            (Path(config.base_dir) / path).resolve() 
            for path in paths
        ]
        
        for path in full_path:
            check_file(path)
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
        check_paths([path, filename])

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

async def rename_file(path: str, new_name: str):
    try:
        old_name = path.split('/')[-1]
        old_ext = old_name.split('.')[-1]
        if new_name.count('.') == 0: new_name += f'.{old_ext}'
        
        full_path = (Path(config.base_dir) / path).resolve()
        new_path = (Path(config.base_dir) / new_name).resolve()
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
