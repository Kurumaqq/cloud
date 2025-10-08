from typing import Optional, Literal, List
from pydantic import BaseModel


class DownloadFileErrorResponse(BaseModel):
    status: Literal["error"]
    message: Optional[str] = None


class ListFilesResponse(BaseModel):
    status: Literal["ok", "error"]
    files: Optional[List[dict]] = None
    message: Optional[str] = None


class DeleteFilesResponse(BaseModel):
    status: Literal["ok", "error"]
    files: Optional[str]
    message: Optional[str] = None


class UploadFileResponse(BaseModel):
    status: Literal["ok", "error"]
    filename: Optional[str]
    message: Optional[str] = None


class ReadFileResponse(BaseModel):
    status: Literal["ok", "error"]
    content: Optional[str] = None
    message: Optional[str] = None


class RenameFileResponse(BaseModel):
    status: Literal["ok", "error"]
    old_name: Optional[str] = None
    new_name: Optional[str] = None
    message: Optional[str] = None


class GetFileErrorResponse(BaseModel):
    status: Literal["error"]
    filename: Optional[str] = None
    message: Optional[str] = None


class CopyFileResponse(BaseModel):
    status: Literal["ok", "error"]
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str]


class MoveFileResponse(BaseModel):
    status: Literal["ok", "error"]
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None


class UploadChunkResponse(BaseModel):
    status: Literal["ok"]
    chunkIndex: Optional[int] = None
    message: Optional[str] = None


class CompleteUploadResponse(BaseModel):
    status: Literal["ok"]
    filename: Optional[str] = None
    message: Optional[str] = None

class AddFavouriteResponse(BaseModel):
    status: Literal["ok"]
    filename: Optional[str] = None
    message: Optional[str] = None

class DeleteFavouriteResponse(BaseModel):
    status: Literal["ok"]
    filename: Optional[str] = None
    message: Optional[str] = None
