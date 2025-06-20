from src.schemas.dirs import *
from src.errors.dirs import * 
from pathlib import Path
from src.config import Config
import shutil
from src.utils import check_path

config = Config()

async def list_dirs(path: str):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)

        if not full_path.exists() or not full_path.is_dir():
            raise DirsNotFoundHttpError(path)

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

async def create_dir(path: str): 
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)

        if full_path.exists():
            raise DirsExistsHttpError(path)

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

async def delete_dir(path: str):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)

        if not full_path.exists():
            raise DirsNotFoundHttpError(path)

        shutil.rmtree(full_path)
        return DeleteDirResponse(
            status='ok',
            message=f'Directory {path} deleted successfully.'
        )

    except Exception as e:
        return DeleteDirResponse(
            status='error',
            message=str(e)
        )
