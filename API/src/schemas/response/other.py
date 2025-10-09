from typing import List, Optional, Literal
from pydantic import BaseModel

class ListCombinedResponse(BaseModel):
    status: Literal['ok', 'error']
    dirs: Optional[List[str]] = None
    files: Optional[List[str]] = None
    all: Optional[List[str]] = None
    message: Optional[str]

class GetDiskResponse(BaseModel):
    status: Literal['ok', 'error']
    disk_total: Optional[float] = None
    disk_used: Optional[float] = None
    message: Optional[str]
