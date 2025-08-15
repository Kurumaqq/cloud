from typing import List, Optional, Literal
from pydantic import BaseModel

class ListDirsResponse(BaseModel):
    status: Literal['ok', 'error'] 
    dirs: Optional[List[str]] = None
    message: Optional[str] = None

class CreateDirResponse(BaseModel):
    status: Literal['ok', 'error']
    message: str

class DeleteDirResponse(BaseModel):
    status: Literal['ok', 'error']
    dir: Optional[str]
    message: Optional[str]

class RenameDirResponse(BaseModel):
    status: Literal['ok', 'error']
    old_name: Optional[str]
    new_name: Optional[str]
    message: Optional[str]

class CopyDirResponse(BaseModel):
    status: Literal['ok', 'error']
    old_path: Optional[str]
    new_path: Optional[str]
    name: Optional[str] = None
    message: Optional[str]

class SizeDirResponse(BaseModel):
    status: Literal['ok', 'error']
    size: Optional[float] = None
    type: Optional[str] = None
    message: Optional[str]
