from src.utils import check_path, check_file, check_paths, check_token, chunk_generator, unique_name, copy_file_thread
from fastapi.responses import FileResponse, StreamingResponse
from src.errors.dirs import NotDirHttpError
from fastapi import UploadFile, Request, Form, Query
from mimetypes import guess_type
from src.schemas.files import *
from src.errors.files import *
from src.config import Config
from pathlib import Path
import asyncio
import shutil
import os
from urllib.parse import unquote

config = Config()

def resolve_path(path: str) -> Path:
    decoded_path = unquote(path)
    return (Path(config.base_dir) / decoded_path).resolve()

async def list_files(path: str, request: Request) -> ListFilesResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_dir = resolve_path(path)
        check_path(path)

        if not src_dir.is_dir():
            raise NotDirHttpError(path)

        files = [f.name for f in src_dir.iterdir() if f.is_file()]

        return ListFilesResponse(
            status='ok',
            files=files,
            message='Files listed successfully.'
        )
    except Exception as e:
        return ListFilesResponse(
            status='error',
            message=str(e)
        )

async def download_file(path: str, token: str = Query(...)) -> FileResponse | DownloadFileErrorResponse:
    try:
        check_token(token) 

        src_file = resolve_path(path)
        check_path(path)
        check_file(src_file)

        return FileResponse(
            path=str(src_file),
            media_type="application/octet-stream",
            filename=src_file.name,  
        )
    except Exception as e:
        return DownloadFileErrorResponse(
            status="error",
            message=str(e)
        )

async def delete_file(path: str , request: Request) -> DeleteFilesResponse: 
    try: 
        token = request.headers['Authorization']
        check_token(token)

        src_file = resolve_path(path)
        check_path(path)
        check_file(src_file)

        src_file.unlink()

        return DeleteFilesResponse(
            status='ok',
            files=src_file.name,
            message=f'File {src_file.name} deleted successfully.'
        )
    except Exception as e:
        return DeleteFilesResponse(
            status='error',
            files=path,
            message=str(e)
        )

async def upload_chunk(
    request: Request,
    file: UploadFile,
    uploadId: str = Form(...),
    chunkIndex: int = Form(...),
    totalChunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/")
):
    token = request.headers.get("Authorization")
    check_token(token)

    temp_dir = Path("tmp") / uploadId
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_path = temp_dir / f"{chunkIndex:05d}.part"
    with open(chunk_path, "wb") as f:
        while content := await file.read(10 * 1024 * 1024):
            f.write(content)

    return {"status": "ok", "chunkIndex": chunkIndex}

async def complete_upload(
    request: Request,
    uploadId: str = Form(...),
    totalChunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/")
):
    token = request.headers.get("Authorization")
    check_token(token)

    # Папка назначения
    target_dir = resolve_path(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / filename

    temp_dir = Path("tmp") / uploadId
    temp_dir.mkdir(parents=True, exist_ok=True) 
    print(f"Temporary directory: {temp_dir}")

    # Объединяем чанки
    with open(target_file, "wb") as outfile:
        for i in range(totalChunks):
            chunk_path = temp_dir / f"{i:05d}.part"
            if not chunk_path.exists():
                raise FileNotFoundError(f"Chunk not found: {chunk_path}")
            with open(chunk_path, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    # Удаляем временные файлы
    shutil.rmtree(temp_dir)

    return {
        "status": "ok",
        "filename": filename,
        "message": f"File {filename} uploaded successfully to {path}"
    }

async def read_file(path: str, request: Request) -> ReadFileResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)
        print(path)
        src_file = resolve_path(path)
        print(src_file)
        check_path(path)
        check_file(src_file)

        with open(src_file, 'r', encoding='utf-8') as f:
            data = f.read()

        return ReadFileResponse(
            status='ok',
            content=data,
            message=f'File {src_file.name} read successfully.'
        )
    except Exception as e: 
        return ReadFileResponse(
            status='error',
            message=str(e)
        )

async def rename_file(path: str, new_name: str, request: Request) -> RenameFileResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        decoded_path = unquote(path)
        decoded_new_name = unquote(new_name)

        src_file = resolve_path(decoded_path)
        old_name = src_file.name
        old_ext = Path(old_name).suffix

        new_name_only = Path(decoded_new_name).name
        if '.' not in new_name_only:
            new_name_only += old_ext

        dst_file = src_file.parent / new_name_only

        check_paths([decoded_path, new_name_only])
        check_file(src_file)

        src_file.rename(dst_file)

        return RenameFileResponse(
            status='ok',
            old_name=old_name,
            new_name=new_name_only,
            message=f'File {old_name} renamed to {new_name_only} successfully.'
        )
    except Exception as e:
        return RenameFileResponse(
            status='error',
            old_name=old_name if 'old_name' in locals() else "",
            new_name=new_name if 'new_name' in locals() else "",
            message=str(e)
        )

async def copy_file(file_path: str, copy_path: str, request: Request) -> CopyFileResponse:
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_file = resolve_path(file_path)
        dst_file = resolve_path(copy_path)

        check_paths([file_path, copy_path])
        check_file(src_file)

        target_path = unique_name(dst_file, src_file.name, 'file')
        await copy_file_thread(src_file, target_path)

        return CopyFileResponse(
            status='ok',
            old_path=file_path,
            new_path=copy_path,
            name=target_path.name,
            message=f'File {src_file.name} copied to {copy_path} successfully.'
        )
    except Exception as e:
        return CopyFileResponse(
            status='error',
            old_path=file_path,
            new_path=copy_path,
            message=str(e)
        )

async def get_file(path: str, request: Request):
    try:
        token = request.headers['Authorization']
        check_token(token)

        src_file = resolve_path(path)
        check_path(path)

        filename = src_file.name
        mime_type = guess_type(filename)[0] or "application/octet-stream"
        file_size = os.path.getsize(src_file)
        chunk_size = 5 * 1024 * 1024

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
        }

        return StreamingResponse(
            chunk_generator(src_file, chunk_size),
            headers=headers,
            media_type=mime_type,
        )
    except Exception as e:
        return GetFileErrorResponse(
            status='error',
            filename=path.split('/')[-1],
            message=str(e)
        )
