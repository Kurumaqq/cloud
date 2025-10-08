from pydantic import BaseModel
from fastapi import Form

class MoveFileRequest(BaseModel):
    path: str
    move_path: str


class ChunkForm(BaseModel):
    upload_id: str
    chunk_index: int
    total_chunks: int
    filename: str
    path: str

    @classmethod
    def as_form(
        cls,
        upload_id: str = Form(...),
        chunk_index: int = Form(...),
        total_chunks: int = Form(...),
        filename: str = Form(...),
        path: str = Form(...),
    ):
        return cls(
            upload_id=upload_id,
            chunk_index=chunk_index,
            total_chunks=total_chunks,
            filename=filename,
            path=path,
        )


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
