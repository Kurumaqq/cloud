from fastapi import APIRouter
from src import services
from src.schemas.login import LoginRequest

router = APIRouter(prefix='/login', tags=['login'])

@router.post('/')
async def login(data: LoginRequest):
   return await services.login(data)
