from pydantic import BaseModel
from typing import List, Optional, Literal

class ListDirsResponse(BaseModel):
    status: Literal['ok', 'error'] 
    dirs: Optional[List[str]] = None
    message: Optional[str] = None

class CreateDirResponse(BaseModel):
    status: Literal['ok', 'error']
    message: str

class DeleteDirResponse(BaseModel):
    status: Literal['ok', 'error']
    message: str

class RenameDirResponse(BaseModel):
    status: Literal['ok', 'error']
    old_name: str
    new_name: str
    message: str
