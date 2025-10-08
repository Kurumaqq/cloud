from pydantic import BaseModel
from typing import Optional

class LoginResponse(BaseModel):
    message: Optional[str]
    uuid: Optional[str]
    username: Optional[str]
