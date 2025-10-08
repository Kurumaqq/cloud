from src.utils import (
    check_path,
    check_dir,
    check_paths,
    check_token,
    size_convert,
    unique_name,
    copy_dir_thread,
    resolve_path,
)
from src.schemas.dirs import *
from src.errors.dirs import *
from src.config import Config
from fastapi import Request, Response
import platform
import stat
import os
import shutil

config = Config()


async def list_dirs(
    path: str, 
    request: Request, 
    response: Response
) -> ListDirsResponse:
    await check_token(request, response)

    src_dir = resolve_path(path)
    check_path(path)
    check_dir(src_dir)

    dirs = [f.name for f in src_dir.iterdir() if f.is_dir()]
    return ListDirsResponse(status="ok", dirs=dirs, message="Dirs listed successfully.")


async def size_dir(path: str, request: Request, response: Response) -> SizeDirResponse:
    await check_token(request, response)
    check_path(path)

    src_dir = resolve_path(path)
    check_dir(src_dir)

    size = 0
    for f in src_dir.glob("**/*"):
        if f.is_file():
            if platform.system() == "Linux":
                size += f.stat().st_blocks
            else:
                ize += f.stat().st_size

    result = size_convert(size)
    return SizeDirResponse(
        status="ok",
        size=result["size"],
        type=result["type"],
        message=f"Directory {src_dir.name} size calculated.",
    )


async def create_dir(
    path: str, request: Request, response: Response
) -> CreateDirResponse:
    await check_token(request, response)
    check_path(path)

    src_dir = resolve_path(path)
    src_dir.mkdir(parents=True, exist_ok=False)
    return CreateDirResponse(
        status="ok", message=f"Directory {src_dir.name} created successfully."
    )


async def rename_dir(
    path: str, new_path: str, request: Request, response: Response
) -> RenameDirResponse:
    await check_token(request, response)
    check_paths([path, new_path])

    new_name = resolve_path(new_path).name
    src_dir = resolve_path(path)
    old_name = src_dir.name
    dst_dir = src_dir.parent / new_path
    check_dir(src_dir)

    dst_dir.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(src_dir, dst_dir)
    return RenameDirResponse(
        status="ok",
        old_name=old_name,
        new_name=new_name,
        message=f"Directory {old_name} renamed to {new_name} successfully.",
    )


async def copy_dir(
    dir_path: str, copy_path: str, request: Request, response: Response
) -> CopyDirResponse:
    await check_token(request, response)
    check_paths([dir_path, copy_path])

    src_dir = resolve_path(dir_path)
    dst_dir = resolve_path(copy_path)
    check_dir(src_dir)

    target_path = unique_name(dst_dir, src_dir.name, "dir")
    name = target_path.name

    await copy_dir_thread(src_dir, target_path)

    return CopyDirResponse(
        status="ok",
        old_path=dir_path,
        new_path=copy_path,
        name=name,
        message=f"Directory {src_dir.name} copied to {copy_path} successfully.",
    )


async def delete_dir(
    path: str, request: Request, response: Response
) -> DeleteDirResponse:
    await check_token(request, response)
    check_path(path)

    src_dir = resolve_path(path)
    check_dir(src_dir)

    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE) 
        func(path)

    shutil.rmtree(src_dir, onerror=remove_readonly)

    return DeleteDirResponse(
        status="ok",
        dir=src_dir.name,
        message=f"Directory {src_dir.name} deleted successfully.",
    )
