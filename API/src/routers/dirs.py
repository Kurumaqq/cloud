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
async def list_dirs(path: str) -> ListDirsResponse:
    return await services.list_dirs(path)

@router.get("/size/{path:path}", response_model=SizeDirResponse)
async def size_dir(path: str) -> SizeDirResponse:
    return await services.size_dir(path)

@router.post("/create", response_model=CreateDirResponse)
async def create_dir(path: str) -> CreateDirResponse:
    return await services.create_dir(path)

@router.post("/rename", response_model=RenameDirResponse)
async def rename_dir(data: RenameDirRequest) -> RenameDirResponse:
    return await services.rename_dir(data)

@router.post("/copy", response_model=CopyDirResponse)
async def copy_dir(data: CopyDirRequest) -> CopyDirResponse:
    return await services.copy_dir(data)

@router.post("/add-favourite", response_model=AddFavouriteResponse)
async def add_fav(path: str) -> AddFavouriteResponse:
    return await services.add_fav_dir(path)

@router.post("/rm-favourite", response_model=AddFavouriteResponse)
async def remove_fav(path: str) -> AddFavouriteResponse:
    return await services.remove_fav_dir(path)

@router.delete("/delete", response_model=DeleteDirResponse)
async def delete_dir(path: str) -> DeleteDirResponse:
    return await services.delete_dir(path)
