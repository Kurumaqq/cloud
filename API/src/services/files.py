from src.utils.filesystem import resolve_path, unique_name, copy_file_thread, iter_file
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import UploadFile, Request, Form, File
from src.schemas.response.files import *
from src.schemas.request.files import *
from src.utils.validators import *
from moviepy import VideoFileClip
from src.utils.favourite import (
    check_favourite,
    remove_favourite,
    add_favourite,
    change_favourite,
)
from src.errors.files import *
from src.config import Config
from pathlib import Path
from io import BytesIO
from PIL import Image
import shutil
import os
from redis import asyncio as aioredis
from io import BytesIO
from fastapi.responses import StreamingResponse
from PIL import Image
import os
import av, hashlib, datetime
import aiofiles, asyncio
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

config = Config()
redis = aioredis.Redis(host="127.0.0.1", port=6379, password="1682", db=0)
engine = create_async_engine(
    "postgresql+asyncpg://kurumaqq:1682@192.168.0.12/cloud",
)
# redis = aioredis.Redis(host="192.168.0.12", port=6379, password="1682", db=0)

# TODO: thearding
# TODO: add Depends for auth validation
# TODO: Fix move
async def list_files(path: str, request: Request) -> ListFilesResponse:
    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir)
    validate_dir(src_dir)
    validate_path(path)

    files = [
        {"name": i.name, "favourite": await check_favourite(i, "file"), "size": 0}
        for i in src_dir.iterdir()
        if i.is_file()
    ]

    sorted_files = sorted(files, key=lambda x: (-x["favourite"], x["name"]))
    return ListFilesResponse(
        status="ok", 
        files=sorted_files, 
        message="Files listed successfully."
    )


async def add_fav_file(path: str, request: Request) -> AddFavouriteResponse:
    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    validate_path(path)
    validate_file(src_file)

    await add_favourite(src_file, "file")
    return AddFavouriteResponse(
        status="ok",
        filename=src_file.name,
        message=f"File {src_file.name} added to favourite successfully.",
    )


async def remove_fav_file(path: str, request: Request) -> DeleteFavouriteResponse:
    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    validate_path(path)
    validate_file(src_file)

    await remove_favourite(src_file, "file")
    return DeleteFavouriteResponse(
        status="ok",
        filename=src_file.name,
        message=f"File {src_file.name} removed from favourite successfully.",
    )


async def move_file(data: MoveFileRequest, request: Request) -> MoveFileResponse:
    path = data.path
    move_path = data.move_path

    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    dst_file = resolve_path(move_path)
    await validate_user_dirs(request, dst_file.parent)

    validate_paths([path, move_path])
    validate_file(src_file)

    target_path = unique_name(dst_file, src_file.name, "file")

    # TODO: Return progress
    await copy_file_thread(src_file, target_path)
    os.remove(src_file)

    await change_favourite(str(src_file), str(target_path), "file")
    return MoveFileResponse(
        status="ok",
        old_path=path,
        new_path=str(target_path),
        name=target_path.name,
        message=f"File {src_file.name} moved to {move_path} successfully.",
    )


async def download_file(path: str, request: Request) -> FileResponse:
    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    validate_path(path)
    validate_file(src_file)

    return FileResponse(
        path=str(src_file),
        media_type="application/octet-stream",
        filename=src_file.name,
    )

async def delete_file(path: str, request: Request) -> DeleteFilesResponse:
    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    validate_path(path)
    validate_file(src_file)

    src_file.unlink()
    await remove_favourite(src_file, "file")
    return DeleteFilesResponse(
        status="ok",
        files=src_file.name,
        message=f"File {src_file.name} deleted successfully.",
    )


async def upload_chunk(
    request: Request,
    file: UploadFile = File(...),
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    path: str = Form(...),
):
    src_dir = resolve_path(path)
    await validate_user_dirs(request, src_dir)
    temp_dir = Path("tmp") / upload_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_path = temp_dir / f"{chunk_index:05d}.part"
    with open(chunk_path, "wb") as f:
        while content := await file.read(10 * 1024 * 1024):
            f.write(content)

    return {"status": "ok", "chunkIndex": chunk_index}


async def complete_upload(
    request: Request,
    upload_id: str = Form(...),
    total_chunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/"),
):
    target_dir = resolve_path(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / filename
    await validate_user_dirs(request, target_file.parent)
    image_ext = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"}
    ext = os.path.splitext(filename)[1].lower()
    file_type = "pic" if ext in image_ext else "thumb" 
    cache_key = f"{file_type}:{os.path.join(path, filename)}:{250}"

    temp_dir = Path("tmp") / upload_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(target_file, "wb") as outfile:
        async for i in range(total_chunks):
            chunk_path = temp_dir / f"{i:05d}.part"
            if not chunk_path.exists():
                raise FileNotFoundError(f"Chunk not found: {chunk_path}")
            with aiofiles.open(chunk_path, "rb") as infile:
                while True:
                    chunk = await infile.read(1024 * 1024)
                    if not chunk: break
                    await outfile.write(chunk)

    async with aiofiles.open(target_file, 'rb') as f:
        content = await f.read()
        await redis.set(cache_key, content)


    # TODO: Thread 
    shutil.rmtree(temp_dir)
    return UploadChunkResponse(
        status="ok",
        filename=filename,
        message="Upload chunk is successful"
    )

async def read_file(path: str, request: Request) -> ReadFileResponse:
    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    validate_path(path)
    validate_file(src_file)

    with open(src_file, "r", encoding="utf-8") as f:
        data = f.read()

    return ReadFileResponse(
        status="ok",
        content=data,
        message=f"File {src_file.name} read successfully.",
    )

async def rename_file(data: RenameFileRequest, request: Request) -> RenameFileResponse:
    path = data.path
    new_name = data.new_name

    validate_paths([path, new_name])

    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    old_name = src_file.name
    old_ext = Path(old_name).suffix

    validate_file(src_file)

    new_name_only = Path(new_name).name
    if "." not in new_name_only:
        new_name_only += old_ext

    dst_file = src_file.parent / new_name_only

    src_file.rename(dst_file)
    await change_favourite(str(src_file), str(dst_file), "file")
    return RenameFileResponse(
        status="ok",
        old_name=old_name,
        new_name=new_name_only,
        message=f"File {old_name} renamed to {new_name_only} successfully.",
    )


async def copy_file(data: CopyFileRequest, request: Request) -> CopyFileResponse:
    path = data.path
    copy_path = data.copy_path

    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    dst_file = resolve_path(copy_path)

    validate_paths([path, copy_path])
    validate_file(src_file)

    target_path = unique_name(dst_file, src_file.name, "file")
    await copy_file_thread(src_file, target_path)

    await change_favourite(str(src_file), str(target_path), "file")
    return CopyFileResponse(
        status="ok",
        old_path=path,
        new_path=copy_path,
        name=target_path.name,
        message=f"File {src_file.name} copied to {copy_path} successfully.",
    )


async def get_file(path: str, request: Request, width: int = None):
    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)
    file_size = os.path.getsize(src_file)
    ext = os.path.splitext(src_file)[1].lower()
    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    cache_key = f"pic:{path}:{width}"
    cached = await redis.get(cache_key)
    if cached:
        headers = {
            "Cache-Control": "public, max-age=2592000",
            "ETag": f'"{hashlib.md5(cached).hexdigest()}"',
            "Last-Modified": datetime.datetime.utcfromtimestamp(
                os.path.getmtime(src_file)
            ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        await redis.expire(cache_key, 60 * 60 * 24 * 180)
        return StreamingResponse(
            BytesIO(cached), 
            media_type="image/png", 
            headers=headers
            )

    if ext in image_extensions:
        def process_image(w):
            with Image.open(src_file) as img: 
                if w:
                    w = max(1, int(w))
                    aspect_ratio = img.height / img.width
                    height = max(1, int(width * aspect_ratio))
                    img = img.resize((width, height))

                buf = BytesIO()
                img_format = img.format or "PNG"

                if img_format.upper() in {"JPEG", "JPG"} and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                if img_format.upper() in {"JPEG", "JPG"}:
                    img.save(buf, format="JPEG")
                    media_type = "image/jpeg"
                else:
                    img.save(buf, format="PNG")
                    media_type = "image/png"

                buf.seek(0)
                data = buf.getvalue()

            headers = {
                "Cache-Control": "public, max-age=2592000",
                "ETag": f'"{hashlib.md5(data).hexdigest()}"',
                "Last-Modified": datetime.datetime.utcfromtimestamp(
                    os.path.getmtime(src_file)
                ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
            }
            return data, headers, media_type 
        
        data, headers, media_type = await asyncio.to_thread(process_image, width)
        await redis.set(cache_key, data, ex=60 * 60 * 24 * 180)
        return StreamingResponse(
            BytesIO(data), 
            media_type=media_type, 
            headers=headers
            )

    range_header = request.headers.get("range")

    if range_header:
        byte_range = range_header.replace("bytes=", "").split("-")
        start = int(byte_range[0])
        end = int(byte_range[1]) if byte_range[1] else file_size - 1
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
        }
        return StreamingResponse(
            iter_file(file_size, src_file, start),
            status_code=206,
            headers=headers,
            media_type="video/mp4",
        )
    else:
        headers = {"Content-Length": str(file_size), "Accept-Ranges": "bytes"}
        return StreamingResponse(
            iter_file(file_size, src_file, 0),
            headers=headers,
            media_type="video/mp4",
        )


async def gen_video_thumb(data: GenVideoThumbRequest, request: Request) -> StreamingResponse:
    path = data.path
    time = float(data.time)
    width = int(data.width)

    src_file = resolve_path(path)
    await validate_user_dirs(request, src_file.parent)

    cache_key = f"thumb:{path}:{width}"
    cached = await redis.get(cache_key)
    if cached:
        headers = {
            "Cache-Control": "public, max-age=2592000",
            "ETag": f'"{hashlib.md5(cached).hexdigest()}"',
            "Last-Modified": datetime.datetime.utcfromtimestamp(
                os.path.getmtime(src_file)
            ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        await redis.expire(cache_key, 60 * 60 * 24 * 180)
        return StreamingResponse(BytesIO(cached), media_type="image/webp", headers=headers)

    container = av.open(src_file)
    stream = container.streams.video[0]

    container.seek(int(time * stream.average_rate))

    frame = None
    for packet in container.demux(stream):
        for video_frame in packet.decode():
            if video_frame.pts is not None:
                frame_time = float(video_frame.pts * video_frame.time_base)
                if frame_time >= time:
                    frame = video_frame
                    break
        if frame:
            break

    if frame is None:
        raise RuntimeError("No frame found at given time")

    img = frame.to_image()

    w_percent = width / float(img.width)
    h_size = int(float(img.height) * w_percent)
    img = img.resize((width, h_size), Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="WEBP", lossless=True)
    buf.seek(0)
    data = buf.getvalue()

    headers = {
        "Cache-Control": "public, max-age=2592000",
        "ETag": f'"{hashlib.md5(data).hexdigest()}"',
        "Last-Modified": datetime.datetime.utcfromtimestamp(
            os.path.getmtime(src_file)
        ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }
    await redis.set(cache_key, data, ex=60 * 60 * 24 * 180)
    return StreamingResponse(buf, media_type="image/webp", headers=headers)
