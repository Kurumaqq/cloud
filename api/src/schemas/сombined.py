from pydantic import BaseModel
from typing import List, Optional, Literal

class ListCombinedResponse(BaseModel):
    status: Literal['ok', 'error']
    dirs: Optional[List[str]] = None
    files: Optional[List[str]] = None
    all: Optional[List[str]] = None
    message: Optional[str] = None
