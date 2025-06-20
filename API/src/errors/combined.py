from fastapi.exceptions import HTTPException

class InvalidPathHttpError(HTTPException):
    def __init__(self, path=''):
        super().__init__(
            status_code=400, 
            detail=f'Invalid path: {path}'
            )
class PathTraversalHttpError(HTTPException):
    def __init__(self, path=''):
        super().__init__(
            status_code=403, 
            detail=f'Path traversal detected: {path}'
            )
class InvalidToken(HTTPException):
    def __init__(self, token=''):
        super().__init__(
            status_code=401, 
            detail=f'Invalid token {token}'
            )
