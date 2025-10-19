from src.schemas.response.dirs import *
from src.schemas.request.dirs import *
from src.utils.favourite import *
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
import os, asyncio

config = Config()

# TODO: thearding
async def async_iterdir(path: Path):
    loop = asyncio.get_event_loop()
    for entry in await loop.run_in_executor(None, lambda: list(path.iterdir())):
        yield entry

async def list_dirs(path: str, request: Request) -> ListDirsResponse:
    src_dir = resolve_path(path)
    validate_path(path)
    validate_dir(src_dir)

    dirs = []
    async for i in async_iterdir(src_dir): 
        if i.is_dir():
            try:
                await validate_user_dirs(request, i)
                dirs.append({
                    "name": i.name,
                    "favourite": await check_favourite(i, "dir"),
                    "size": 0
                })
            except HTTPException:
                continue

    sorted_dirs = sorted(dirs, key=lambda x: (-x["favourite"], x["name"]))

    return ListDirsResponse(
        status="ok", dirs=sorted_dirs, message="Dirs listed successfully."
    )


async def size_dir(path: str) -> SizeDirResponse:
    src_dir = resolve_path(path)
    validate_dir(src_dir)

    size = 0
    for f in src_dir.glob("**/*"):
        if f.is_file():
            if platform.system() == "Linux":
                size += f.stat().st_blocks
            else:
                zize += f.stat().st_size

    result = size_convert(size)
    return SizeDirResponse(
        status="ok",
        size=result["size"],
        type=result["type"],
        message=f"Directory {src_dir.name} size calculated.",
    )


async def create_dir(path: str, request: Request) -> CreateDirResponse:
    validate_path(path)
    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir.parent)

    src_dir = resolve_path(path)
    src_dir.mkdir(parents=True, exist_ok=False)
    return CreateDirResponse(
        status="ok", message=f"Directory {src_dir.name} created successfully."
    )


async def rename_dir(data: RenameDirRequest, request: Request) -> RenameDirResponse:
    path = data.path
    new_name = data.new_name
    validate_paths([path, new_name])

    src_new_name = resolve_path(new_name).name
    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir.parent)
    old_name = src_dir.name
    dst_dir = src_dir.parent / src_new_name
    validate_dir(src_dir)

    dst_dir.parent.mkdir(parents=True, exist_ok=True)

    await change_favourite(path, new_name, "dir")
    # TODO: Thread 
    shutil.move(src_dir, dst_dir)
    return RenameDirResponse(
        status="ok",
        old_name=old_name,
        new_name=src_new_name,
        message=f"Directory {old_name} renamed to {src_new_name} successfully.",
    )


async def copy_dir(data: CopyDirRequest, request: Request) -> CopyDirResponse:
    dir_path = data.dir_path
    copy_path = data.copy_path

    validate_paths([dir_path, copy_path])

    src_dir = resolve_path(dir_path)
    await validate_user_dirs(request, src_dir.parent)
    dst_dir = resolve_path(copy_path)
    validate_dir(src_dir)

    target_path = unique_name(dst_dir, src_dir.name, "dir")
    name = target_path.name

    # TODO: Thread
    await copy_dir_thread(src_dir, target_path)
    return CopyDirResponse(
        status="ok",
        old_path=dir_path,
        new_path=copy_path,
        name=name,
        message=f"Directory {src_dir.name} copied to {copy_path} successfully.",
    )


async def delete_dir(path: str, request: Request) -> DeleteDirResponse:
    validate_path(path)

    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir.parent)
    validate_dir(src_dir)

    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    # TODO: Thread
    shutil.rmtree(src_dir, onerror=remove_readonly)
    return DeleteDirResponse(
        status="ok",
        dir=src_dir.name,
        message=f"Directory {src_dir.name} deleted successfully.",
    )


async def add_fav_dir(path: str, request: Request) -> AddFavouriteResponse:
    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir.parent)
    validate_path(path)
    validate_dir(src_dir)

    await add_favourite(path, "dir")
    return AddFavouriteResponse(
        status="ok",
        filename=src_dir.name,
        message=f"Directory {src_dir.name} added to favourite successfully.",
    )

async def remove_fav_dir(path: str, request: Request) -> DeleteFavouriteResponse:
    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir.parent)
    validate_path(path)
    validate_dir(src_dir)

    await remove_favourite(path, "dir")
    return DeleteFavouriteResponse(
        status="ok",
        filename=src_dir.name,
        message=f"Directory {src_dir.name} removed from favourite successfully.",
    )
