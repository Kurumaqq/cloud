from fastapi.exceptions import HTTPException

class InvalidPasswordOrUserHttpError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401, 
            detail='invalid username or password'
            )  
