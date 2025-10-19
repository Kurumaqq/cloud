from src.utils.filesystem import resolve_path
from src.utils.validators import *
from src.errors.other import *
from src.config import Config
from src.schemas.response.other import *
import shutil
import psutil
import platform

config = Config()

async def disk() -> GetDiskResponse:
    partitions = psutil.disk_partitions(all=False)
    disk_total = 0
    disk_used = 0
    GB = 2**30

    if platform.system() == "Windows":
        for partition in partitions:
            usage = shutil.disk_usage(partition.mountpoint)
            disk_total += usage.total
            disk_used += usage.used
    elif platform.system() == "Linux":
        disk_info = shutil.disk_usage("/")
        disk_total = disk_info.total
        disk_used = disk_info.used

    disk_total_gb = round(disk_total / GB, 2)
    disk_used_gb = round(disk_used / GB, 2)
    return GetDiskResponse(
        status="ok",
        disk_total=disk_total_gb,
        disk_used=disk_used_gb,
        message=f"Total disk space: {disk_total_gb}GB, used: {disk_used_gb}GB",
    )
