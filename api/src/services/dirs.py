from src.utils import check_path, check_dir, check_paths, check_token
from src.schemas.dirs import *
from src.errors.dirs import * 
from src.config import Config
from pathlib import Path
import shutil
from fastapi import Request

config = Config()

async def list_dirs(path: str, request: Request) -> ListDirsResponse:
    try:
        token = request.headers['Authorization']
        full_path = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)
        check_dir(full_path)

        dirs = [
            str(f.as_posix()) 
            for f in full_path.iterdir() 
            if f.is_dir()
            ]
        return ListDirsResponse(
            status='ok',
            dirs=dirs,
            message='Dirs listed successfully.'
        )
    except Exception as e:
        return ListDirsResponse(
            status='error',
            message=str(e)
        )

async def create_dir(path: str, request: Request) -> CreateDirResponse: 
    try:
        token = request.headers['Authorization']
        full_path = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)
        check_dir(full_path)

        full_path.mkdir(parents=True, exist_ok=False)
        return CreateDirResponse(
            status='ok',
            message=f'Directory {path} created successfully.'
        )
    
    except Exception as e:
        return CreateDirResponse(
            status='error',
            message=str(e)
        )

async def delete_dir(path: str, request: Request) -> DeleteDirResponse:
    try:
        token = request.headers['Authorization']
        full_path = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)
        check_dir(full_path)

        shutil.rmtree(full_path)
        return DeleteDirResponse(
            status='ok',
            dir=path,
            message=f'Directory {path} deleted successfully.'
        )

    except Exception as e:
        return DeleteDirResponse(
            status='error',
            dir=path,
            message=str(e)
        )

async def rename_dir(path: str, new_name: str, request: Request) -> RenameDirResponse:
    try:
        token = request.headers['Authorization']
        old_name = Path(path).name
        full_path = (Path(config.base_dir) / path).resolve()
        parent_path = Path(path).parent
        new_path = (Path(config.base_dir) / parent_path / new_name).resolve()
        
        check_token(token)
        check_paths([path, new_name])
        check_dir(full_path)

        shutil.move(full_path, new_path)

        return RenameDirResponse(
            status='ok',
            old_name=old_name,
            new_name=new_name,
            message=f'Directory {path} renamed to {new_name} successfully.'
        )
    except Exception as e:
        return RenameDirResponse(
            status='error',
            old_name=old_name,
            new_name=new_name,
            message=str(e)
        )
