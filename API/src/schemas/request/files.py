from pydantic import BaseModel
from fastapi import Form

class MoveFileRequest(BaseModel):
    path: str
    move_path: str

class RenameFileRequest(BaseModel):
    path: str
    new_name: str

class CopyFileRequest(BaseModel):
    path: str
    copy_path: str

class GenVideoThumbRequest(BaseModel):
    path: str
    time: float = 0.5
    width: int = 100
