import json
from pathlib import Path
from src.config import Config
import aiofiles 
# TODO: DRY

config = Config()
async def check_favourite(path, t):
    base_dir = Path(config.base_dir)
    async with aiofiles.open(config.path, "r") as f:
        content = await f.read()
    data = json.loads(content)
    if str(base_dir / path) in data["favourite"][f"{t}s"]:
        return True

    return False

async def add_favourite(path, t):
    base_dir = Path(config.base_dir)
    src_path = str(base_dir / path)
    async with aiofiles.open(config.path, "r") as f:
        content = await f.read()
    data = json.loads(content)
    if src_path in data["favourite"][f"{t}s"]:
        return {"status": "error", "message": f"{path} is already exists"}
    data["favourite"][f"{t}s"].append(src_path)
    async with aiofiles.open(config.path, "w") as f:
        await f.write(json.dumps(data, indent=4))

async def remove_favourite(path, t):
    base_dir = Path(config.base_dir)
    src_path = str(base_dir / path)
    async with aiofiles.open(config.path, "r") as f:
        content = await f.read()
        data = json.loads(content)
    if src_path not in data["favourite"][f"{t}s"]:
        return {"status": "error", "message": f"{path} is not exists"}
    data["favourite"][f"{t}s"].remove(src_path)
    async with aiofiles.open(config.path, "w") as f:
        await f.write(json.dumps(data, indent=4))

async def change_favourite(path, new_value, t):
    base_dir = Path(config.base_dir)
    src_path = str(base_dir / path)
    src_new_path = str(base_dir / new_value)
    async with aiofiles.open(config.path, "r") as f:
        content = await f.read()
        data = json.loads(content)
        for i in range(len(data["favourite"][f"{t}s"])):
            if  data["favourite"][f"{t}s"][i] == src_path:
                data["favourite"][f"{t}s"][i] = src_new_path
                async with aiofiles.open(config.path, "w") as f:
                    await f.write(json.dumps(data, indent=4))
                return {"status": "ok"}
