from .dirs import router as dirs_router
from .files import router as files_router
from .сombined import router as combined_router
from fastapi import APIRouter

master_router = APIRouter()

master_router.include_router(dirs_router)
master_router.include_router(files_router)
master_router.include_router(combined_router)
