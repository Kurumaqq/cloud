from src.config import Config
from src.errors.combined import InvalidPathHttpError, PathTraversalHttpError
from pathlib import Path

config = Config()

def check_path(path: str) -> bool:
    base_resolved = Path(config.base_dir).resolve()

    if '..' in path or Path(path).is_absolute():
        raise InvalidPathHttpError(path)

    path_resolved = (Path(config.base_dir) / path).resolve()
    base_resolved = Path(config.base_dir).resolve()
    if not str(path_resolved).startswith(str(base_resolved)):
        raise PathTraversalHttpError(path)

    return True
