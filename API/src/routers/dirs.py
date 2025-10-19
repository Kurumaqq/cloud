from fastapi import APIRouter, Request, Response, Depends
from src.schemas.response.dirs import *
from src.schemas.request.dirs import *
from src import services
from src.utils.validators import validate_auth

router = APIRouter(
    prefix="/dirs", 
    tags=["dirs"], 
    dependencies=[Depends(validate_auth)]
    )

@router.get("/list/{path:path}", response_model=ListDirsResponse)
async def list_dirs(path: str, request: Request) -> ListDirsResponse:
    return await services.list_dirs(path, request)

@router.get("/size/{path:path}", response_model=SizeDirResponse)
async def size_dir(path: str) -> SizeDirResponse:
    return await services.size_dir(path)

@router.post("/create", response_model=CreateDirResponse)
async def create_dir(path: str, request: Request) -> CreateDirResponse:
    return await services.create_dir(path, request)

@router.post("/rename", response_model=RenameDirResponse)
async def rename_dir(data: RenameDirRequest, request: Request) -> RenameDirResponse:
    return await services.rename_dir(data, request)

@router.post("/copy", response_model=CopyDirResponse)
async def copy_dir(data: CopyDirRequest, request: Request) -> CopyDirResponse:
    return await services.copy_dir(data, request)


@router.post("/add-favourite", response_model=AddFavouriteResponse)
async def add_fav(path: str, request: Request) -> AddFavouriteResponse:
    return await services.add_fav_dir(path, request)

@router.post("/rm-favourite", response_model=AddFavouriteResponse)
async def remove_fav(path: str, request: Request) -> AddFavouriteResponse:
    return await services.remove_fav_dir(path, request)

@router.delete("/delete", response_model=DeleteDirResponse)
async def delete_dir(path: str, request: Request) -> DeleteDirResponse:
    return await services.delete_dir(path, request)
