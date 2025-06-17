from pydantic import BaseModel
from typing import List, Optional, Literal

class ListFilesResponse(BaseModel):
    status: Literal['ok', 'error'] 
    files: Optional[List[str]] = None
    message: Optional[str] = None

class CreateDirResponse(BaseModel):
    status: Literal['ok', 'error']
    dir_name: str
    message: str
