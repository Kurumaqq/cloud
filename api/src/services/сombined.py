from pathlib import Path
from src.config import Config
from src.errors.combined import *
from src.errors.dirs import DirNotFoundHttpError
from src.utils import check_path
from src.schemas import *

config = Config()

async def combined_list(path: str):
    try:
        full_path = (Path(config.base_dir) / path).resolve()
        check_path(path)

        if not full_path.exists() or not full_path.is_dir():
            raise DirNotFoundHttpError(path)

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
