from src.utils.filesystem import resolve_path, unique_name, copy_file_thread, iter_file
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import UploadFile, Request, Form, Response, File
from src.errors.dirs import NotDirHttpError
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

config = Config()


async def list_files(
    path: str, request: Request, response: Response
) -> ListFilesResponse:
    await validate_auth(request, response)
    
    src_dir = resolve_path(path)
    validate_path(path)

    if not src_dir.is_dir():
        raise NotDirHttpError(path)

    files = []

    for i in src_dir.iterdir():
        if i.is_file():
            favourite = check_favourite(src_dir / i.name, "file")
            files.append(
                {
                    "name": i.name,
                    "favourite": favourite,
                    "size": 0,
                }
            )

    sorted_files = sorted(files, key=lambda x: (-x["favourite"], x["name"]))

    return ListFilesResponse(
        status="ok", files=sorted_files, message="Files listed successfully."
    )


async def add_fav_file(
    path: str, request: Request, response: Response
) -> AddFavouriteResponse:
    await validate_auth(request, response)
    src_file = resolve_path(path)
    validate_path(path)
    validate_file(src_file)

    add_favourite(src_file, "file")

    return AddFavouriteResponse(
        status="ok",
        filename=src_file.name,
        message=f"File {src_file.name} added to favourite successfully.",
    )


async def remove_fav_file(
    path: str, request: Request, response: Response
) -> DeleteFavouriteResponse:
    await validate_auth(request, response)
    src_file = resolve_path(path)
    validate_path(path)
    validate_file(src_file)

    remove_favourite(src_file, "file")

    return DeleteFavouriteResponse(
        status="ok",
        filename=src_file.name,
        message=f"File {src_file.name} removed from favourite successfully.",
    )


async def move_file(
    data: MoveFileRequest, request: Request, response: Response
) -> MoveFileResponse:
    await validate_auth(request, response)

    path = data.path
    move_path = data.move_path

    src_file = resolve_path(path)
    dst_file = resolve_path(move_path)

    validate_paths([path, move_path])
    validate_file(src_file)

    target_path = unique_name(dst_file, src_file.name, "file")

    await copy_file_thread(src_file, target_path)
    os.remove(src_file)

    if check_favourite(str(src_file), "file"):
        change_favourite(str(src_file), str(target_path), "file")

    return MoveFileResponse(
        status="ok",
        old_path=path,
        new_path=str(target_path),
        name=target_path.name,
        message=f"File {src_file.name} moved to {move_path} successfully.",
    )


async def download_file(
    path: str, request: Request, response: Response
) -> FileResponse:
    await validate_auth(request, response)

    src_file = resolve_path(path)
    validate_path(path)
    validate_file(src_file)

    return FileResponse(
        path=str(src_file),
        media_type="application/octet-stream",
        filename=src_file.name,
    )


async def delete_file(
    path: str, request: Request, response: Response
) -> DeleteFilesResponse:
    await validate_auth(request, response)

    src_file = resolve_path(path)
    validate_path(path)
    validate_file(src_file)

    src_file.unlink()
    if check_favourite(src_file, "file"):
        remove_favourite(src_file, "file")

    return DeleteFilesResponse(
        status="ok",
        files=src_file.name,
        message=f"File {src_file.name} deleted successfully.",
    )


async def upload_chunk(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
):
    await validate_auth(request, response)

    temp_dir = Path("tmp") / upload_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_path = temp_dir / f"{chunk_index:05d}.part"
    with open(chunk_path, "wb") as f:
        while content := await file.read(10 * 1024 * 1024):
            f.write(content)

    return {"status": "ok", "chunkIndex": chunk_index}


async def complete_upload(
    request: Request,
    response: Response,
    upload_id: str = Form(...),
    total_chunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/"),
):
    await validate_auth(request, response)

    target_dir = resolve_path(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / filename

    temp_dir = Path("tmp") / upload_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    with open(target_file, "wb") as outfile:
        for i in range(total_chunks):
            chunk_path = temp_dir / f"{i:05d}.part"
            if not chunk_path.exists():
                raise FileNotFoundError(f"Chunk not found: {chunk_path}")
            with open(chunk_path, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    shutil.rmtree(temp_dir)

    return UploadChunkResponse(
        status="ok", filename=filename, message="Upload chunk is successfull"
    )


async def read_file(
    path: str,
    request: Request,
    response: Response,
) -> ReadFileResponse:
    await validate_auth(request, response)
    src_file = resolve_path(path)
    validate_path(path)
    validate_file(src_file)

    with open(src_file, "r", encoding="utf-8") as f:
        data = f.read()

    return ReadFileResponse(
        status="ok",
        content=data,
        message=f"File {src_file.name} read successfully.",
    )


async def rename_file(
    data: RenameFileRequest,
    request: Request,
    response: Response,
) -> RenameFileResponse:
    await validate_auth(request, response)
    path = data.path
    new_name = data.new_name

    validate_paths([path, new_name_only])
    validate_file(src_file)

    src_file = resolve_path(path)
    old_name = src_file.name
    old_ext = Path(old_name).suffix

    new_name_only = Path(new_name).name
    if "." not in new_name_only:
        new_name_only += old_ext

    dst_file = src_file.parent / new_name_only

    src_file.rename(dst_file)
    change_favourite(str(src_file), str(dst_file), "file")

    return RenameFileResponse(
        status="ok",
        old_name=old_name,
        new_name=new_name_only,
        message=f"File {old_name} renamed to {new_name_only} successfully.",
    )


async def copy_file(
    data: CopyFileRequest,
    request: Request,
    response: Response,
) -> CopyFileResponse:
    await validate_auth(request, response)
    path = data.path
    copy_path = data.copy_path

    src_file = resolve_path(path)
    dst_file = resolve_path(copy_path)

    validate_paths([path, copy_path])
    validate_file(src_file)

    target_path = unique_name(dst_file, src_file.name, "file")
    await copy_file_thread(src_file, target_path)

    if check_favourite(str(src_file), "file"):
        change_favourite(str(src_file), str(target_path), "file")

    return CopyFileResponse(
        status="ok",
        old_path=path,
        new_path=copy_path,
        name=target_path.name,
        message=f"File {src_file.name} copied to {copy_path} successfully.",
    )


async def get_file(
    path: str,
    request: Request,
    response: Response,
    width: int = None,
):
    await validate_auth(request, response)
    src_file = resolve_path(path)
    file_size = os.path.getsize(src_file)
    ext = os.path.splitext(src_file)[1].lower()
    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    if ext in image_extensions:
        with Image.open(src_file) as img:
            if width:
                width = max(1, int(width))
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

        return StreamingResponse(buf, media_type=media_type)

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
        return StreamingResponse(iter_file(), headers=headers, media_type="video/mp4")


async def gen_video_thumb(
    data: GenVideoThumbRequest, request: Request, response: Response
) -> StreamingResponse:
    path = data.path
    time = data.time
    width = data.width

    await validate_auth(request, response)

    src_file = resolve_path(path)
    validate_file(src_file)

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
