from pathlib import Path
from src.schemas import *
from src.config import Config

config = Config()

async def get_list_files(path: str):
    try:
        if '..' in path or Path(path).is_absolute():
            raise ValueError("Invalid path: '..' or absolute paths are not allowed.")

        dir_path = (Path(config.base_dir) / path).resolve()
        base_dir_resolved = Path(config.base_dir).resolve()
        if not str(dir_path).startswith(str(base_dir_resolved)):
            raise ValueError("Invalid path: Directory traversal detected.")

        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f"Directory {path} does not exist.")

        files = [str(f.as_posix()) for f in dir_path.iterdir()]
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

async def create_dir(path: str): 
    try:
        if '..' in path or Path(path).is_absolute():
            raise ValueError("Invalid path: '..' or absolute paths are not allowed.")

        full_path = (Path(config.base_dir) / path).resolve()

        base_dir_resolved = Path(config.base_dir).resolve()
        if not str(full_path).startswith(str(base_dir_resolved)):
            raise ValueError("Invalid path: Directory traversal detected.")

        if full_path.exists():
            raise FileExistsError(f"Directory {path} already exists.")

        full_path.mkdir(parents=True, exist_ok=False)
        return CreateDirResponse(
            status='ok',
            dir_name=str(full_path),
            message=f'Directory {path} created successfully.'
        )
    
    except Exception as e:
        return CreateDirResponse(
            status='error',
            dir_name=str(full_path) if 'full_path' in locals() else path,
            message=str(e)
        )
