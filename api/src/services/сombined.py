from src.utils import check_path, check_dir, check_token
from src.errors.combined import *
from src.config import Config
from fastapi import Request
from src.schemas import *
from pathlib import Path

config = Config()

async def combined_list(path: str, request: Request):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_path(path)
        check_dir(full_path)

        dirs = []
        files = []
        for i in full_path.iterdir():
            if i.is_file(): files.append(str(i.as_posix()))
            elif i.is_dir(): dirs.append(str(i.as_posix()))

        return ListCombinedResponse(
            status='ok',
            dirs=dirs,
            files=files,
            all=dirs + files,
            message='Dirs and files listed successfully.'
        )
    except Exception as e:
        return ListCombinedResponse(
            status='error',
            message=str(e)
        )
