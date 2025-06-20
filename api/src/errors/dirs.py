from fastapi.exceptions import HTTPException

class DirsNotFoundHttpError(HTTPException):
    def __init__(self, path: str):
        super().__init__(
            status_code=404, 
            detail=f"Directories not found: {path}"
            )

class DirsExistsHttpError(HTTPException):
    def __init__(self, path: str):
        super().__init__(
            status_code=409, 
            detail=f"Directories already exist: {path}"
            )

class NotDirHttpError(HTTPException):
    def __init__(self, path: str):
        super().__init__(
            status_code=400, 
            detail=f"Path is not a directory: {path}"
            )   
