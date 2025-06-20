from src.schemas.сombined import *
from fastapi import APIRouter
from src import services 

router = APIRouter(prefix='/combined', tags=['Combined'])

@router.get('/list/{path:path}', response_model=ListCombinedResponse)
async def combined_list(path: str) -> ListCombinedResponse:     
    return await services.combined_list(path)
