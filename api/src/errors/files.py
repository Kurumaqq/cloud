from fastapi import HTTPException

class FileNotFoundHttpError(HTTPException):
    def __init__(self, path=''):
        super().__init__(
            status_code=404, 
            detail=f'File not found: {path}'
            )
class NotFileHttpError(HTTPException):
    def __init__(self, path=''):
        super().__init__(
            status_code=400, 
            detail=f'Path is not a file: {path}'
            )

class FileExistsHttpError(HTTPException):
    def __init__(self, path=''):
        super().__init__(
            status_code=400, 
            detail=f'File already exists: {path}'
            )   
