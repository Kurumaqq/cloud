from src.utils.favourite import check_favourite, add_favourite, remove_favourite
from src.schemas.response.dirs import *
from src.schemas.request.dirs import *
from fastapi import Request, Response
from src.utils.filesystem import (
    resolve_path,
    size_convert,
    unique_name,
    copy_dir_thread,
)
from src.utils.validators import *
from src.config import Config
from src.errors.dirs import *
import platform
import shutil
import stat
import os

config = Config()


async def list_dirs(
    path: str, request: Request, response: Response
) -> ListDirsResponse:
    await validate_auth(request, response)

    src_dir = resolve_path(path)
    validate_path(path)
    validate_dir(src_dir)

    dirs = []

    for i in src_dir.iterdir():
        if i.is_dir():
            favourite = check_favourite(i, "dir")
            print(i)
            dirs.append(
                {
                    "name": i.name,
                    "favourite": favourite,
                    "size": 0,
                }
            )

    sorted_dirs = sorted(dirs, key=lambda x: (-x["favourite"], x["name"]))

    return ListDirsResponse(
        status="ok", dirs=sorted_dirs, message="Dirs listed successfully."
    )


async def size_dir(path: str, request: Request, response: Response) -> SizeDirResponse:
    await validate_auth(request, response)
    validate_path(path)

    src_dir = resolve_path(path)
    validate_dir(src_dir)

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
    await validate_auth(request, response)
    validate_path(path)

    src_dir = resolve_path(path)
    src_dir.mkdir(parents=True, exist_ok=False)
    return CreateDirResponse(
        status="ok", message=f"Directory {src_dir.name} created successfully."
    )


async def rename_dir(
    data: RenameDirRequest, request: Request, response: Response
) -> RenameDirResponse:
    await validate_auth(request, response)
    path = data.path
    new_name = data.new_name
    validate_paths([path, new_name])

    src_new_name = resolve_path(new_name).name
    src_dir = resolve_path(path)
    old_name = src_dir.name
    dst_dir = src_dir.parent / src_new_name
    validate_dir(src_dir)

    dst_dir.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(src_dir, dst_dir)
    return RenameDirResponse(
        status="ok",
        old_name=old_name,
        new_name=src_new_name,
        message=f"Directory {old_name} renamed to {src_new_name} successfully.",
    )


async def copy_dir(
    data: CopyDirRequest, request: Request, response: Response
) -> CopyDirResponse:
    await validate_auth(request, response)
    dir_path = data.dir_path
    copy_path = data.copy_path

    validate_paths([dir_path, copy_path])

    src_dir = resolve_path(dir_path)
    dst_dir = resolve_path(copy_path)
    validate_dir(src_dir)

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
    await validate_auth(request, response)
    validate_path(path)

    src_dir = resolve_path(path)
    validate_dir(src_dir)

    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(src_dir, onerror=remove_readonly)

    return DeleteDirResponse(
        status="ok",
        dir=src_dir.name,
        message=f"Directory {src_dir.name} deleted successfully.",
    )


async def add_fav_dir(
    path: str, request: Request, response: Response
) -> AddFavouriteResponse:
    await validate_auth(request, response)
    src_dir = resolve_path(path)
    validate_path(path)
    validate_dir(src_dir)

    add_favourite(path, "dir")
    return AddFavouriteResponse(
        status="ok",
        filename=src_dir.name,
        message=f"Directory {src_dir.name} added to favourite successfully.",
    )


async def remove_fav_dir(
    path: str, request: Request, response: Response
) -> DeleteFavouriteResponse:
    await validate_auth(request, response)
    src_dir = resolve_path(path)
    validate_path(path)
    validate_dir(src_dir)

    remove_favourite(path, "dir")
    return DeleteFavouriteResponse(
        status="ok",
        filename=src_dir.name,
        message=f"Directory {src_dir.name} removed from favourite successfully.",
    )
