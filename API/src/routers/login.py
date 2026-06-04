from src.schemas.request.other import UserRequest
from fastapi import APIRouter, Response
from src import services


router = APIRouter(tags=["login"])

@router.post("/login")
async def login(data: UserRequest, response: Response):
    return await services.login(data, response)


@router.post("/logout")
async def logout(response: Response):
    return await services.logout(response)
