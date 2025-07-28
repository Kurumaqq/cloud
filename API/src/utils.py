from src.errors.combined import InvalidPathHttpError, PathTraversalHttpError, InvalidToken
from src.errors.files import FileNotFoundHttpError, NotFileHttpError
from src.errors.dirs import DirNotFoundHttpError, NotDirHttpError
from src.config import Config
from pathlib import Path
import asyncio
import shutil

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

async def chunk_generator(path, chunk_size):
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk: break
                    yield chunk

     
def size_convert(value: int):
     types = {
         -1: 'bytes ',
          0: 'KB',
          1: 'MB',
          2: 'GB'
     }
     for i in range(3):
        print(i)
        if value / 1024 > 1: 
            value /= 1024
            print(value)
        else: 
            print(i)
            print(value)
            value = int(value * 100) / 100
            return {'size': value, 'type': types[i-1]}

def unique_name(dst: Path, name: str, t: str) -> Path:
    target_path = dst / name
    counter = 1
    FILE_TYPE = 'file'
    DIR_TYPE = 'dir'
    while target_path.exists():
        if t == DIR_TYPE:
            target_path = dst / f"{name}_{counter}"
        elif t == FILE_TYPE:
            if '.' in name:
                name_part, ext = name.rsplit('.', 1)
                target_path = dst / f"{name_part}_{counter}.{ext}"
            else:
                target_path = dst / f"{name}_{counter}"
        counter += 1
    return target_path

async def copy_dir_thread(src: Path, dst: Path):
    await asyncio.to_thread(shutil.copytree, src, dst)
    return dst

async def copy_file_thread(src: Path, dst: Path):
    await asyncio.to_thread(shutil.copy, src, dst)
    return dst
