from src.utils import check_path, check_dir, check_token
from src.errors.combined import *
from src.config import Config
from fastapi import Request
from src.schemas import *
from pathlib import Path
import shutil
import psutil
import platform

config = Config()

async def combined_list(path: str, request: Request) -> ListCombinedResponse:
    try:
        src_dir = (Path(config.base_dir) / path).resolve()
        token = request.headers['Authorization']

        check_token(token)
        check_path(path)
        check_dir(src_dir)

        dirs = []
        files = []
        for i in src_dir.iterdir():
            if i.is_file(): files.append(str(i.as_posix()))
            elif i.is_dir(): dirs.append(str(i.as_posix()))

        return ListCombinedResponse(
            status='ok',
            dirs=dirs,
            files=files,
            all=dirs + files,
            message='Dirs and files listed successfully.'
        )
    except Exception as e:
        return ListCombinedResponse(
            status='error',
            message=str(e)
        )

async def disk(request: Request) -> GetDiskResponse:
    try: 
        token = request.headers['Authorization']
        partitions = psutil.disk_partitions(all=False)
        disk_total = 0
        disk_used = 0
        GB = 2**30 

        check_token(token)
        
        if platform.system() == 'Windows':
            for partition in partitions:
                usage = shutil.disk_usage(partition.mountpoint)
                disk_total += usage.total
                disk_used += usage.used
        elif platform.system() == 'Linux':
            disk_info = shutil.disk_usage('/')
            disk_total = disk_info.total
            disk_used = disk_info.used

        disk_total_gb = round(disk_total / GB, 2)
        disk_used_gb = round(disk_used / GB, 2)
        return GetDiskResponse(
            status='ok',
            disk_total=disk_total_gb,
            disk_used=disk_used_gb,
            message=f'Total disk space: {disk_total_gb}GB, used: {disk_used_gb}GB'
        )
    except Exception as e:
        return GetDiskResponse(
            status='error',
            disk_total=0,
            disk_used=0,
            message=str(e)
        )
