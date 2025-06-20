from fastapi import APIRouter
from src import services 
from src.schemas.сombined import *

router = APIRouter(prefix='/combined', tags=['Combined'])

@router.get('/list/{path:path}', response_model=ListCombinedResponse)
async def combined_list(path: str):     
    return await services.combined_list(path)
