from fastapi import APIRouter
from src.crud import *
from src.schemas import *

router = APIRouter(prefix='/dirs', tags=['dirs'])

@router.get('/list/{path:path}', response_model=ListFilesResponse)
async def list_files(path: str): return await get_list_files(path)

#TODO: POST AND CHECK EXISTS 
@router.post('/create', response_model=CreateDirResponse)
async def create_directory(path: str):
    return await create_dir(path)

# #TODO: DELETE AND CHECK EXISTS 
# @router.get('/delete/{path:path}')
# async def delete_dir(name: str):    
#     os.rmdir(f'C:/dev/server_status/{name}')
#     return {'status': 'ok', 'message': f'Directory {name} deleted successfully.'}
