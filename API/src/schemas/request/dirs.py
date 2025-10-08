from pydantic import BaseModel

class CopyDirRequest(BaseModel):
    dir_path: str
    copy_path: str

class RenameDirRequest(BaseModel):
    path: str
    new_name: str
