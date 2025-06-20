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
