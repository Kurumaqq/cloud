from fastapi import HTTPException, Request, Response
from src.config import Config, config_authx, authx
from authx.exceptions import AuthXException
from pathlib import Path
import bcrypt
from src.errors import (
    PathTraversalHttpError, 
    FileNotFoundHttpError, 
    NotFileHttpError, 
    DirNotFoundHttpError, 
    NotDirHttpError,
    InvalidCredentialsHttpError,
    )

config = Config()

def validate_user(username: str, password: str):
    if username != config.username:
        raise InvalidCredentialsHttpError()
    if not validate_password(password, config.password):
        raise InvalidCredentialsHttpError()

    return True

def validate_path(path: str) -> bool:
    path = path.lstrip("/")

    if ".." in path:
        raise PathTraversalHttpError(path)

    base_path = Path(config.base_dir).resolve()
    abs_path = (base_path / path).resolve()

    if not str(abs_path).startswith(str(base_path)):
        raise PathTraversalHttpError(path)

    return True


def validate_paths(paths: list[str]) -> bool:
    for path in paths:
        validate_path(path)
    return True


def validate_file(path: Path) -> bool:
    if not path.exists():
        raise FileNotFoundHttpError(path)
    if not path.is_file():
        raise NotFileHttpError(path)

    return True


def validate_dir(path: Path) -> bool:
    if not path.exists():
        raise DirNotFoundHttpError(path)
    if not path.is_dir():
        raise NotDirHttpError(path)

    return True


def validate_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password)


async def validate_auth(request: Request, response: Response):
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
                    int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
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
