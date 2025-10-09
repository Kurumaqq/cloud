from src.schemas.request.other import UserRequest
from fastapi import APIRouter, Response
from src import services


router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
async def login(data: UserRequest, response: Response):
    return await services.login(data, response)
