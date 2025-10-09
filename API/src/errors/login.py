from fastapi.exceptions import HTTPException


class InvalidCredentialsHttpError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="invalid username or password")
