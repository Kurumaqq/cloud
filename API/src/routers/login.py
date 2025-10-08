from fastapi import APIRouter, Response
from src import services
from src.schemas.request.login import UserRequest
from src.schemas.response.login import LoginResponse
from pydantic import BaseModel


router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
async def login(data: UserRequest, response: Response):
    return await services.login(data, response)
