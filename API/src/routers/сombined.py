from src.schemas.сombined import *
from fastapi import APIRouter, Request, Response
from src import services 

router = APIRouter(prefix='/combined', tags=['Combined'])

@router.get('/list/{path:path}', response_model=ListCombinedResponse)
async def combined_list(path: str, request: Request, response: Response) -> ListCombinedResponse:     
    return await services.combined_list(path, request, response)


@router.get('/disk', response_model=GetDiskResponse)
async def disk(request: Request, response: Response) -> GetDiskResponse:
    return await services.disk(request, response)
