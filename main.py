from fastapi import FastAPI
import uvicorn
from pathlib import Path

app = FastAPI()

@app.get('/get-files-name')
async def get_files_name():
    path = Path('C:/dev/cloud')
    files = [str(i).replace('\\', '/') for i in path.iterdir()]
    return {'status': 'ok', 'files': files}

@app.get('/get-files-name/{dir}')
async def get_files_name_from_dir(dir: str):
    path  = Path(f'C:/dev/cloud/{dir.replace('+', '/')}')
    files = [str(i).replace('\\', '/') for i in path.iterdir()]
    return {'status': 'ok', 'dir': dir.replace('+', '/'), 'files': files}

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        reload=True
        )
