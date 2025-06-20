from src.errors.combined import InvalidPathHttpError, PathTraversalHttpError, InvalidToken
from src.errors.files import FileNotFoundHttpError, NotFileHttpError
from src.errors.dirs import DirNotFoundHttpError, NotDirHttpError
from src.config import Config
from pathlib import Path

config = Config()

def check_path(path: str) -> bool:
    if '..' in path or Path(path).is_absolute():
        raise InvalidPathHttpError(path)

    full_path = (Path(config.base_dir) / path).resolve()
    base_path = Path(config.base_dir).resolve()
    if not str(full_path).startswith(str(base_path)):
        raise PathTraversalHttpError(path)

    return True

def check_paths(paths: list[str]) -> bool:
    for path in paths: check_path(path)

    return True

def check_file(path: Path) -> bool:
    if not path.exists():
        raise FileNotFoundHttpError(path)
    if not path.is_file():
        raise NotFileHttpError(path)

    return True

def check_dir(path: Path) -> bool:
    if not path.exists():
        raise DirNotFoundHttpError(path)   
    if not path.is_dir():
        raise NotDirHttpError(path)

    return True

def check_token(token):
    token = f'Bearer {token}'
    if config.token != token: raise InvalidToken(token)

    return True
