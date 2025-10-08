from fastapi import APIRouter, Response
from src import services
from src.schemas.login import LoginRequest
from pydantic import BaseModel


router = APIRouter(prefix="/login", tags=["login"])


class User(BaseModel):
    username: str
    password: str


@router.post("/")
async def login(data: User, response: Response):
    return await services.login_endpoint(data.username, data.password, response)
