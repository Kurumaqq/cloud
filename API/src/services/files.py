from src.utils import (
    check_path,
    check_file,
    check_paths,
    check_token,
    unique_name,
    copy_thread,
    resolve_path
)
from fastapi.responses import FileResponse, StreamingResponse
from src.errors.dirs import NotDirHttpError
from fastapi import UploadFile, Request, Form, Query
from src.schemas.files import *
from src.errors.files import *
from src.config import Config
from pathlib import Path
import shutil
from PIL import Image
import os
from urllib.parse import unquote
from moviepy import VideoFileClip
from io import BytesIO
import os


config = Config()

async def list_files(path: str, request: Request) -> ListFilesResponse:
    check_token(request)

    src_dir = resolve_path(path)
    check_path(path)

    if not src_dir.is_dir():
        raise NotDirHttpError(path)

    files = [f.name for f in src_dir.iterdir() if f.is_file()]

    return ListFilesResponse(
        status="ok", files=files, message="Files listed successfully."
    )


async def move_file(path: str, move_path: str, request: Request) -> MoveFileResponse:
    check_token(request)

    src_file = resolve_path(path)
    dst_file = resolve_path(move_path)

    check_paths([path, move_path])
    check_file(src_file)

    target_path = unique_name(dst_file, src_file.name, "file")

    await copy_thread(src_file, target_path)
    os.remove(src_file)

    return MoveFileResponse(
        status="ok",
        old_path=path,
        new_path=str(target_path),
        name=target_path.name,
        message=f"File {src_file.name} moved to {move_path} successfully.",
    )


async def download_file(path: str, token: str = Query(...)) -> FileResponse:
    check_token(token)

    src_file = resolve_path(path)
    check_path(path)
    check_file(src_file)

    return FileResponse(
        path=str(src_file),
        media_type="application/octet-stream",
        filename=src_file.name,
    )


async def delete_file(path: str, request: Request) -> DeleteFilesResponse:
    check_token(request)

    src_file = resolve_path(path)
    check_path(path)
    check_file(src_file)

    src_file.unlink()

    return DeleteFilesResponse(
        status="ok",
        files=src_file.name,
        message=f"File {src_file.name} deleted successfully.",
    )


async def upload_chunk(
    request: Request,
    file: UploadFile,
    uploadId: str = Form(...),
    chunkIndex: int = Form(...),
):
    check_token(request)

    temp_dir = Path("tmp") / uploadId
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_path = temp_dir / f"{chunkIndex:05d}.part"
    with open(chunk_path, "wb") as f:
        while content := await file.read(10 * 1024 * 1024):
            f.write(content)

    return UploadChunkResponse(
        status="ok", chunkIndex=chunkIndex, message="Upload chunk is successfull"
    )


async def complete_upload(
    request: Request,
    uploadId: str = Form(...),
    totalChunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/"),
):
    check_token(request)

    target_dir = resolve_path(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / filename

    temp_dir = Path("tmp") / uploadId
    temp_dir.mkdir(parents=True, exist_ok=True)

    with open(target_file, "wb") as outfile:
        for i in range(totalChunks):
            chunk_path = temp_dir / f"{i:05d}.part"
            if not chunk_path.exists():
                raise FileNotFoundError(f"Chunk not found: {chunk_path}")
            with open(chunk_path, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    shutil.rmtree(temp_dir)

    return UploadChunkResponse(
        status="ok", filename=filename, message="Upload chunk is successfull"
    )


async def read_file(path: str, request: Request) -> ReadFileResponse:
    check_token(request)
    src_file = resolve_path(path)
    check_path(path)
    check_file(src_file)

    with open(src_file, "r", encoding="utf-8") as f:
        data = f.read()

    return ReadFileResponse(
        status="ok",
        content=data,
        message=f"File {src_file.name} read successfully.",
    )


async def rename_file(path: str, new_name: str, request: Request) -> RenameFileResponse:
    check_token(request)

    decoded_path = unquote(path)
    decoded_new_name = unquote(new_name)

    src_file = resolve_path(decoded_path)
    old_name = src_file.name
    old_ext = Path(old_name).suffix

    new_name_only = Path(decoded_new_name).name
    if "." not in new_name_only:
        new_name_only += old_ext

    dst_file = src_file.parent / new_name_only

    check_paths([decoded_path, new_name_only])
    check_file(src_file)

    src_file.rename(dst_file)

    return RenameFileResponse(
        status="ok",
        old_name=old_name,
        new_name=new_name_only,
        message=f"File {old_name} renamed to {new_name_only} successfully.",
    )


async def copy_file(
    file_path: str, copy_path: str, request: Request
) -> CopyFileResponse:
    check_token(request)

    src_file = resolve_path(file_path)
    dst_file = resolve_path(copy_path)

    check_paths([file_path, copy_path])
    check_file(src_file)

    target_path = unique_name(dst_file, src_file.name, "file")
    await copy_thread(src_file, target_path)

    return CopyFileResponse(
        status="ok",
        old_path=file_path,
        new_path=copy_path,
        name=target_path.name,
        message=f"File {src_file.name} copied to {copy_path} successfully.",
    )


async def get_file(path: str, request: Request, token: str):
    check_token(token)
    src_file = resolve_path(path)
    file_size = os.path.getsize(src_file)
    range_header = request.headers.get("range")

    def iter_file(start=0, end=file_size):
        with open(src_file, "rb") as f:
            f.seek(start)
            bytes_to_send = end - start + 1
            chunk_size = 10 * 1024 * 1024
            while bytes_to_send > 0:
                read_size = min(chunk_size, bytes_to_send)
                data = f.read(read_size)
                if not data:
                    break
                bytes_to_send -= len(data)
                yield data

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
            iter_file(start, end),
            status_code=206,
            headers=headers,
            media_type="video/mp4",
        )
    else:
        headers = {"Content-Length": str(file_size), "Accept-Ranges": "bytes"}
        return StreamingResponse(iter_file(), headers=headers, media_type="video/mp4")


class ThumbnailResponse(BaseModel):
    status: str
    file_path: str
    message: str


async def generate_video_thumbnail(
    path: str, request: Request, time: float = 0.5, width: int = 200
) -> StreamingResponse:

    check_token(request)

    src_file = resolve_path(path)
    check_file(src_file)

    clip = VideoFileClip(src_file)
    frame = clip.get_frame(time)
    clip.close()

    image = Image.fromarray(frame)
    w_percent = width / float(image.width)
    h_size = int((float(image.height) * float(w_percent)))
    image = image.resize((width, h_size), Image.LANCZOS)

    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
