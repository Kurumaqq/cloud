from src.schemas.response.other import *
from fastapi import APIRouter, Request, Response, Depends
from src.utils.validators import validate_auth
from src import services 

router = APIRouter(
    prefix='/combined', 
    tags=['Combined'], 
    dependencies=[Depends(validate_auth)]
    )

@router.get('/disk', response_model=GetDiskResponse)
async def disk(request: Request, response: Response) -> GetDiskResponse:
    return await services.disk(request, response)
