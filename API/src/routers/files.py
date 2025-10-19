from fastapi import UploadFile, File, Request, Form
from fastapi import APIRouter, UploadFile, Request, Response
from fastapi.responses import StreamingResponse
from src.schemas.response.files import *
from src.schemas.request.files import *
from src.config import Config
from fastapi import Depends
from src.utils.validators import validate_auth
from src import services

router = APIRouter(
    prefix="/files", 
    tags=["files"], 
    dependencies=[Depends(validate_auth)]
    )
config = Config()

@router.get("/download/{path:path}")
async def download_file(path: str, request: Request) -> DownloadFileErrorResponse:
    return await services.download_file(path, request)

@router.get("/list/{path:path}", response_model=ListFilesResponse)
async def list_files(path: str, request: Request) -> ListFilesResponse:
    return await services.list_files(path, request)


@router.get("/read/{path:path}", response_model=ReadFileResponse)
async def read_file(path: str, request: Request) -> ReadFileResponse:
    return await services.read_file(path, request)


@router.get("/get/{path:path}")
async def get_file(
    path: str,
    request: Request,
    width: int = None,
) -> StreamingResponse:
    return await services.get_file(path, request, width)

@router.get("/thumbnail/{path:path}")
async def thumbnail(
    request: Request,
    path: str,
    time: float = 0.5,
    width: int = 200,
):
    data = GenVideoThumbRequest(path=path, time=time, width=width)
    return await services.gen_video_thumb(data, request)

@router.post("/add-favourite", response_model=AddFavouriteResponse)
async def add_fav(path: str, request: Request) -> AddFavouriteResponse:
    return await services.add_fav_file(path, request)

@router.post("/rm-favourite", response_model=AddFavouriteResponse)
async def remove_fav(path: str, request: Request) -> AddFavouriteResponse:
    return await services.remove_fav_file(path, request)

@router.post("/upload")
async def upload_files(
    request: Request,
    file: UploadFile = File(...),
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    path: str = Form(...)
):
    return await services.upload_chunk(request, file, upload_id, chunk_index, path)

@router.post("/complete-upload")
async def complete_upload(
    request: Request,
    upload_id: str = Form(...),
    total_chunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/"),
):
    return await services.complete_upload(
        request, upload_id, total_chunks, filename, path
    )

@router.post("/rename", response_model=RenameFileResponse)
async def rename_file(data: RenameFileRequest, request: Request) -> RenameFileResponse:
    return await services.rename_file(data, request)

@router.post("/move", response_model=MoveFileResponse)
async def move_file(data: MoveFileRequest, request: Request) -> MoveFileResponse:
    return await services.move_file(data, request)

@router.post("/copy", response_model=CopyFileResponse)
async def copy_file(data: CopyFileRequest, request: Request) -> CopyFileResponse:
    return await services.copy_file(data, request)

@router.delete("/delete", response_model=DeleteFilesResponse)
async def delete_file(path: str, request: Request) -> DeleteFilesResponse:
    return await services.delete_file(path, request)
