from src.utils import check_path, check_dir, check_paths, check_token, size_convert, unique_name, copy_dir_thread
from src.schemas.dirs import *
from src.errors.dirs import * 
from src.config import Config
from fastapi import Request
from pathlib import Path
import platform
import shutil
import asyncio

config = Config()

async def list_dirs(path: str, request: Request) -> ListDirsResponse:
    try:
        token = request.headers['Authorization']
        src_dir = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)
        check_dir(src_dir)

        dirs = [
            str(f.as_posix()) 
            for f in src_dir.iterdir() 
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

async def size_dir(path: str, request: Request)-> SizeDirResponse:
    try:
       size = 0
       token = request.headers['Authorization']
       src_dir = (Path(config.base_dir) / path).resolve()
       check_token(token)
       check_path(path)
       check_dir(src_dir)

       for f in src_dir.glob('**/*'):
           if f.is_file():
               if platform.system() == 'Linux':
                   size += f.stat().st_block
               else:
                   size += f.stat().st_size

       result = size_convert(size)


       return SizeDirResponse(
           status='ok',
           size=result['size'],
           type=result['type'],
           message=f'File {path} weighs a {size}'
       )
    except Exception as e: 
        return SizeDirResponse(
           status='error',
           message=str(e)
       )

async def create_dir(path: str, request: Request) -> CreateDirResponse: 
    try:
        token = request.headers['Authorization']
        src_dir = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)

        src_dir.mkdir(parents=True, exist_ok=False)
        return CreateDirResponse(
            status='ok',
            message=f'Directory {path} created successfully.'
        )
    
    except Exception as e:
        return CreateDirResponse(
            status='error',
            message=str(e)
        )

async def rename_dir(path: str, new_name: str, request: Request) -> RenameDirResponse:
    try:
        token = request.headers['Authorization']
        old_name = Path(path).name
        src_dir = (Path(config.base_dir) / path).resolve()
        parent_path = Path(path).parent
        new_path = (Path(config.base_dir) / parent_path / new_name).resolve()
        
        check_token(token)
        check_paths([path, new_name])
        check_dir(src_dir)

        shutil.move(src_dir, new_path)

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
    
async def copy_dir(dir_path: str, copy_path: str, request: Request) -> CopyDirResponse:
    try:
        token = request.headers['Authorization']
        src_dir = (Path(config.base_dir) / dir_path).resolve()
        dst_dir = (Path(config.base_dir) / copy_path).resolve()

        check_token(token)
        check_paths([dir_path, copy_path])
        check_dir(src_dir)

        dir_name = src_dir.name
        target_path = unique_name(dst_dir, dir_name, 'dir')
        name = target_path.name

        await copy_dir_thread(src_dir, target_path)
        return CopyDirResponse(
            status='ok',
            old_path=dir_path,
            new_path=copy_path,
            name=name,
            message=f'Directory {dir_path} copied to {copy_path} successfully.'
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
        src_dir = (Path(config.base_dir) / path).resolve()
        check_token(token)
        check_path(path)
        check_dir(src_dir)

        shutil.rmtree(src_dir)
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

