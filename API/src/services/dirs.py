from src.utils import check_path, check_dir, check_paths, check_token, size_convert, unique_name, copy_dir_thread
from src.schemas.dirs import *
from src.errors.dirs import *
from src.config import Config
from fastapi import Request
from pathlib import Path
import platform
import shutil
import asyncio
from urllib.parse import unquote

config = Config()

def resolve_path(path: str) -> Path:
    """Декодируем URL и возвращаем абсолютный Path внутри base_dir"""
    decoded_path = unquote(path)
    return (Path(config.base_dir) / decoded_path).resolve()

async def list_dirs(path: str, request: Request) -> ListDirsResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_dir = resolve_path(path)
        check_path(path)
        check_dir(src_dir)

        dirs = [f.name for f in src_dir.iterdir() if f.is_dir()]
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

async def size_dir(path: str, request: Request) -> SizeDirResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_dir = resolve_path(path)
        check_path(path)
        check_dir(src_dir)

        size = 0
        for f in src_dir.glob('**/*'):
            if f.is_file():
                if platform.system() == 'Linux':
                    size += f.stat().st_blocks
                else:
                    size += f.stat().st_size

        result = size_convert(size)

        return SizeDirResponse(
            status='ok',
            size=result['size'],
            type=result['type'],
            message=f'Directory {src_dir.name} size calculated.'
        )
    except Exception as e:
        return SizeDirResponse(
            status='error',
            message=str(e)
        )

async def create_dir(path: str, request: Request) -> CreateDirResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_dir = resolve_path(path)
        check_path(path)

        src_dir.mkdir(parents=True, exist_ok=False)

        return CreateDirResponse(
            status='ok',
            message=f'Directory {src_dir.name} created successfully.'
        )
    except Exception as e:
        return CreateDirResponse(
            status='error',
            message=str(e)
        )

async def rename_dir(path: str, new_name: str, request: Request) -> RenameDirResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        decoded_path = unquote(path)
        decoded_new_name = Path(unquote(new_name)).name  # Берём только имя, без вложенных папок

        src_dir = resolve_path(decoded_path)
        old_name = src_dir.name
        dst_dir = src_dir.parent / decoded_new_name

        check_paths([decoded_path, decoded_new_name])
        check_dir(src_dir)

        # Создаём родительскую директорию на случай, если dst не существует (на всякий случай)
        dst_dir.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(src_dir, dst_dir)

        return RenameDirResponse(
            status='ok',
            old_name=old_name,
            new_name=decoded_new_name,
            message=f'Directory {old_name} renamed to {decoded_new_name} successfully.'
        )
    except Exception as e:
        return RenameDirResponse(
            status='error',
            old_name=old_name if 'old_name' in locals() else "",
            new_name=new_name,
            message=str(e)
        )

async def copy_dir(dir_path: str, copy_path: str, request: Request) -> CopyDirResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_dir = resolve_path(dir_path)
        dst_dir = resolve_path(copy_path)

        check_paths([dir_path, copy_path])
        check_dir(src_dir)

        target_path = unique_name(dst_dir, src_dir.name, 'dir')
        name = target_path.name

        await copy_dir_thread(src_dir, target_path)

        return CopyDirResponse(
            status='ok',
            old_path=dir_path,
            new_path=copy_path,
            name=name,
            message=f'Directory {src_dir.name} copied to {copy_path} successfully.'
        )
    except Exception as e:
        return CopyDirResponse(
            status='error',
            old_path=dir_path,
            new_path=copy_path,
            message=str(e)
        )

async def delete_dir(path: str, request: Request) -> DeleteDirResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_dir = resolve_path(path)
        check_path(path)
        check_dir(src_dir)

        shutil.rmtree(src_dir)

        return DeleteDirResponse(
            status='ok',
            dir=src_dir.name,
            message=f'Directory {src_dir.name} deleted successfully.'
        )
    except Exception as e:
        return DeleteDirResponse(
            status='error',
            dir=path,
            message=str(e)
        )
