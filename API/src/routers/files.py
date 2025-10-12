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
async def download_file(path: str) -> DownloadFileErrorResponse:
    return await services.download_file(path)

@router.get("/list/{path:path}", response_model=ListFilesResponse)
async def list_files(path: str) -> ListFilesResponse:
    return await services.list_files(path)

@router.get("/read/{path:path}", response_model=ReadFileResponse)
async def read_file(path: str) -> ReadFileResponse:
    return await services.read_file(path)

@router.get("/get/{path:path}")
async def get_file(
    path: str,
    request: Request,
    width: int = None,
) -> StreamingResponse:
    return await services.get_file(path, request, width)

@router.get("/thumbnail/{path:path}")
async def thumbnail(
    path: str,
    time: float = 0.5,
    width: int = 200,
):
    data = GenVideoThumbRequest(path=path, time=time, width=width)
    return await services.gen_video_thumb(data)

@router.post("/add-favourite", response_model=AddFavouriteResponse)
async def add_fav(path: str) -> AddFavouriteResponse:
    return await services.add_fav_file(path)

@router.post("/rm-favourite", response_model=AddFavouriteResponse)
async def remove_fav(path: str) -> AddFavouriteResponse:
    return await services.remove_fav_file(path)

@router.post("/upload")
async def upload_files(
    file: UploadFile = File(...),
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
):
    return await services.upload_chunk(file, upload_id, chunk_index)

@router.post("/complete-upload")
async def complete_upload(
    upload_id: str = Form(...),
    total_chunks: int = Form(...),
    filename: str = Form(...),
    path: str = Form("/"),
):
    return await services.complete_upload(
        upload_id, total_chunks, filename, path
    )

@router.post("/rename", response_model=RenameFileResponse)
async def rename_file(data: RenameFileRequest) -> RenameFileResponse:
    return await services.rename_file(data)

@router.post("/move", response_model=MoveFileResponse)
async def move_file(data: MoveFileRequest) -> MoveFileResponse:
    return await services.move_file(data)


@router.post("/copy", response_model=CopyFileResponse)
async def copy_file(data: CopyFileRequest) -> CopyFileResponse:
    return await services.copy_file(data)

@router.delete("/delete", response_model=DeleteFilesResponse)
async def delete_file(path: str) -> DeleteFilesResponse:
    return await services.delete_file(path)
