from src.errors.combined import PathTraversalHttpError
from src.errors.files import FileNotFoundHttpError, NotFileHttpError
from src.errors.dirs import DirNotFoundHttpError, NotDirHttpError
from fastapi.exceptions import HTTPException
from src.config import Config, authx, config_authx
from pathlib import Path
from fastapi import Request, Response
import asyncio
import jwt
import bcrypt
import shutil
from authx.exceptions import AuthXException
from jwt import decode, exceptions
from urllib.parse import unquote
import json


config = Config()


def resolve_path(path: str) -> Path:
    if path and path[0] == "/":
        path = path[1:]
    decoded_path = unquote(path)
    return (Path(config.base_dir) / decoded_path).resolve()


def check_path(path: str) -> bool:
    if ".." in path or Path(path).is_absolute():
        raise PathTraversalHttpError(path)

    base_path = Path(config.base_dir).resolve()
    if path.startswith(str(base_path)):
        raise PathTraversalHttpError(path)

    return True


def check_paths(paths: list[str]) -> bool:
    for path in paths:
        check_path(path)
    return True


def check_file(path: Path) -> bool:
    if not path.exists():
        raise FileNotFoundHttpError(path)
    if not path.is_file():
        raise NotFileHttpError(path)

    return True


def check_dir(path: Path) -> bool:
    if not path.exists():
        raise DirNotFoundHttpError(path)
    if not path.is_dir():
        raise NotDirHttpError(path)

    return True


async def check_token(request: Request, response: Response):
    access_token = request.cookies.get(config_authx.JWT_ACCESS_COOKIE_NAME)
    refresh_token = request.cookies.get(config_authx.JWT_REFRESH_COOKIE_NAME)

    if access_token:
        try:
            payload = await authx.access_token_required(request)
            return payload 
        except AuthXException:
            pass

    if refresh_token:
        try:
            payload = await authx.refresh_token_required(request)
            uid = payload.sub

            if response:
                new_access_token = authx.create_access_token(uid=uid)
                authx.set_access_cookies(
                        new_access_token, 
                        response, 
                        int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds())
                        )

                new_refresh_token = authx.create_refresh_token(uid=uid)
                authx.set_refresh_cookies(
                    new_refresh_token,
                    response,
                    int(config_authx.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
                )

            return payload
        except AuthXException:
            raise HTTPException(status_code=401, detail="Session expired")

    raise HTTPException(status_code=401, detail="Not authenticated")


async def chunk_generator(path, chunk_size):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def size_convert(value: int):
    types = {-1: "bytes ", 0: "KB", 1: "MB", 2: "GB"}
    for i in range(3):
        print(i)
        if value / 1024 > 1:
            value /= 1024
            print(value)
        else:
            print(i)
            print(value)
            value = int(value * 100) / 100
            return {"size": value, "type": types[i - 1]}


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


async def copy_dir_thread(src: Path, dst: Path):
    await asyncio.to_thread(shutil.copytree, src, dst)
    return dst


async def copy_thread(src: Path, dst: Path):
    await asyncio.to_thread(shutil.copy, src, dst)
    return dst


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
                print("Hui")
                if data["favourite"]["files"][i] == key:
                    print(key, data["favourite"]["files"][i])
                    data["favourite"]["files"][i] = str(base_dir / new_value)
                    break
        elif t == "dir":
            for i in range(len(data["favourite"]["dirs"])):
                if data["favourite"]["dirs"][i] == key:
                    data["favourite"]["dirs"][i] = str(base_dir / new_value)
                    break
    with open("src/config/config.json", "w") as f:
        json.dump(data, f, indent=4)

def encode_jwt(payload: dict):
    return jwt.encode(payload, config.secret_key, algorithm="RS256")


def decode_jwt(token: str):
    try:
        return decode(token, config.public_key.encode("utf-8"), algorithms=["RS256"])
    except exceptions.DecodeError as e:
        print("JWT DecodeError:", e)
        raise


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password)


async def auto_refresh_access_token(request: Request, response: Response):
    access_token = request.cookies.get(config_authx.JWT_ACCESS_COOKIE_NAME)
    refresh_token = request.cookies.get(config_authx.JWT_REFRESH_COOKIE_NAME)

    if access_token:
        try:
            await authx.access_token_required(request)
            return
        except AuthXException:
            pass

    if refresh_token:
        try:
            payload = await authx.refresh_token_required(request)
            uid = payload.sub

            new_access_token = authx.create_access_token(uid=uid)
            response.set_cookie(
                config_authx.JWT_ACCESS_COOKIE_NAME,
                new_access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            )

            new_refresh_token = authx.create_refresh_token(uid=uid)
            response.set_cookie(
                config_authx.JWT_REFRESH_COOKIE_NAME,
                new_refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=int(config_authx.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
            )
            return
        except AuthXException: 
            raise HTTPException(status_code=401, detail="Session expired")

    raise HTTPException(status_code=401, detail="Not authenticated")
