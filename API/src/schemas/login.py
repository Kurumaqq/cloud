from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: Optional[str] 
    password: Optional[str]

class LoginResponse(BaseModel):
    massage: Optional[str] = 'Login successful'
    token: Optional[str] = None
