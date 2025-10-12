from urllib.parse import unquote
from src.config import Config
from pathlib import Path
import asyncio
import shutil

config = Config()

# TODO: check in resolve_path 

def resolve_path(path: str) -> Path:
    if path and path[0] == "/":
        path = path[1:]
    decoded_path = unquote(path)
    return (Path(config.base_dir) / decoded_path).resolve()


async def chunk_generator(path, chunk_size):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def size_convert(value: int):
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while value >= 1024 and i < len(units) - 1:
        value /= 1024
        i += 1
    return {"size": round(value, 2), "type": units[i]}


def unique_name(dst: Path, name: str, t: str) -> Path:
    target_path = dst / name
    counter = 1
    FILE_TYPE = "file"
    DIR_TYPE = "dir"
    while target_path.exists():
        if t == DIR_TYPE:
            target_path = dst / f"{name}_{counter}"
        elif t == FILE_TYPE:
            if "." in name:
                name_part, ext = name.rsplit(".", 1)
                target_path = dst / f"{name_part}_{counter}.{ext}"
            else:
                target_path = dst / f"{name}_{counter}"
        counter += 1
    return target_path

def iter_file(end, path, start=0):
    with open(path, "rb") as f:
        f.seek(start)
        bytes_to_send = end - start + 1
        chunk_size = 30 * 1024 * 1024
        while bytes_to_send > 0:
            read_size = min(chunk_size, bytes_to_send)
            data = f.read(read_size)
            if not data:
                break
            bytes_to_send -= len(data)
            yield data


async def copy_dir_thread(src: Path, dst: Path):
    await asyncio.to_thread(shutil.copytree, src, dst)
    return dst


async def copy_file_thread(src: Path, dst: Path):
    await asyncio.to_thread(shutil.copy, src, dst)
    return dst
