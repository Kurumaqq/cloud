from typing import Optional, Literal, List
from pydantic import BaseModel
    
class DownloadFileErrorResponse(BaseModel):
    status: Literal['error']
    message: Optional[str] = None

class ListFilesResponse(BaseModel): 
    status: Literal['ok', 'error'] 
    files: Optional[List[str]] = None
    message: Optional[str] = None

class DeleteFilesResponse(BaseModel):
    status: Literal['ok', 'error']
    files: Optional[str]
    message: Optional[str] = None

class UploadFileResponse(BaseModel):
    status: Literal['ok', 'error']
    filename: Optional[str]
    message: Optional[str] = None

class ReadFileResponse(BaseModel):
    status: Literal['ok', 'error']
    content: Optional[str] = None
    message: Optional[str] = None

class RenameFileResponse(BaseModel):
    status: Literal['ok', 'error']
    old_name: Optional[str] = None
    new_name: Optional[str] = None
    message: Optional[str] = None
