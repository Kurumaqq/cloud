from fastapi import UploadFile, File, Request, Query, Form
from fastapi import APIRouter, UploadFile, Request, Response
from fastapi.responses import StreamingResponse
from src.schemas.files import *
from src.config import Config
from src import services

router = APIRouter(prefix="/files", tags=["files"])
config = Config()


@router.get("/download/{path:path}")
async def download_file(
    path: str, request: Request, response: Response,
) -> DownloadFileErrorResponse:
    return await services.download_file(path, request, response)


@router.get("/list/{path:path}", response_model=ListFilesResponse)
async def list_files(path: str, request: Request, response: Response) -> ListFilesResponse:
    return await services.list_files(path, request, response)


@router.post("/add-favourite", response_model=AddFavouriteResponse)
async def add_fav(path: str, request: Request, response: Response) -> AddFavouriteResponse:
    return await services.add_fav(path, request, response)

@router.post("/rm-favourite", response_model=AddFavouriteResponse)
async def remove_fav(path: str, request: Request, response: Response) -> AddFavouriteResponse:
    return await services.remove_fav(path, request, response)


@router.get("/read/{path:path}", response_model=ReadFileResponse)
async def read_file(path: str, request: Request, response: Response) -> ReadFileResponse:
    return await services.read_file(path, request, response)


@router.get("/get/{path:path}")
async def get_file(
    path: str,
    request: Request,
    response: Response,
) -> StreamingResponse:
    return await services.get_file(path, request, response)


@router.post("/upload")
async def upload_files(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    uploadId: str = Form(...),
    chunkIndex: int = Form(...),
):
    return await services.upload_chunk(request, response, file, uploadId, chunkIndex)


@router.get("/complete-upload")
async def complete_upload(
    request: Request,
    response: Response,
    uploadId: str = Query(...),
    totalChunks: int = Query(...),
    filename: str = Query(...),
    path: str = Query("/"),
):
    return await services.complete_upload(
        request, response, uploadId, totalChunks, filename, path
    )


@router.get("/thumbnail/{path:path}")
async def thumbnail(path: str, request: Request, response: Response, time: float = 0.5):
    return await services.generate_video_thumbnail(path, request, response, time)


@router.post("/rename", response_model=RenameFileResponse)
async def rename_file(
    path: str, 
    new_name: str, 
    request: Request, 
    response: Response,
) -> RenameFileResponse:
    return await services.rename_file(path, new_name, request, response)


@router.post("/move", response_model=MoveFileResponse)
async def move_file(
    path: str, 
    move_path: str, 
    request: Request, 
    response: Response,
) -> MoveFileResponse:
    return await services.move_file(path, move_path, request, response)


@router.post("/copy", response_model=CopyFileResponse)
async def copy_file(
    file_path: str, 
    copy_path: str, 
    request: Request,
    response: Response
) -> CopyFileResponse:
    return await services.copy_file(file_path, copy_path, request, response)


@router.delete("/delete", response_model=DeleteFilesResponse)
async def delete_file(
    path: str, 
    request: Request, 
    response: Response
) -> DeleteFilesResponse:
    return await services.delete_file(path, request, response)
