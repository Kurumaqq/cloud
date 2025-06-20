from fastapi import APIRouter
from src import services 

router = APIRouter(prefix="/combined", tags=["Combined"])

@router.get("/list/{path:path}")
async def combined_list(path: str):     
    return await services.combined_list(path)
