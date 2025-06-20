from typing import List, Optional, Literal
from pydantic import BaseModel

class ListCombinedResponse(BaseModel):
    status: Literal['ok', 'error']
    dirs: Optional[List[str]] = None
    files: Optional[List[str]] = None
    all: Optional[List[str]] = None
    message: Optional[str] = None
