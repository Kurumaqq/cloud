import json
from pathlib import Path
from src.config import Config

config = Config()
def check_favourite(path, t):
    base_dir = Path(config.base_dir)
    with open("src/config/config.json", "r") as f:
        data = json.load(f)
        if str(base_dir / path) in data["favourite"]["files"] and t == "file":
            return True
        if str(base_dir / path) in data["favourite"]["dirs"] and t == "dir":
            return True
    return False


def add_favourite(path, t):
    base_dir = Path(config.base_dir)
    with open("src/config/config.json", "r") as f:
        data = json.load(f)
        if t == "file":
            data["favourite"]["files"].append(str(base_dir / path))
        elif t == "dir":
            data["favourite"]["dirs"].append(str(base_dir / path))
    with open("src/config/config.json", "w") as f:
        json.dump(data, f, indent=4)


def remove_favourite(path, t):
    base_dir = Path(config.base_dir)
    with open("src/config/config.json", "r") as f:
        data = json.load(f)
        if t == "file":
            data["favourite"]["files"].remove(str(base_dir / path))
        elif t == "dir":
            data["favourite"]["dirs"].remove(str(base_dir / path))
    with open("src/config/config.json", "w") as f:
        json.dump(data, f, indent=4)


def change_favourite(key, new_value, t):
    base_dir = Path(config.base_dir)
    with open("src/config/config.json", "r") as f:
        data = json.load(f)
        if t == "file":
            for i in range(len(data["favourite"]["files"])):
                if data["favourite"]["files"][i] == key:
                    data["favourite"]["files"][i] = str(base_dir / new_value)
                    break
        elif t == "dir":
            for i in range(len(data["favourite"]["dirs"])):
                if data["favourite"]["dirs"][i] == key:
                    data["favourite"]["dirs"][i] = str(base_dir / new_value)
                    break
    with open("src/config/config.json", "w") as f:
        json.dump(data, f, indent=4)
