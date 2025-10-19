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
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.model.user import User
from sqlalchemy import select

config = Config()
engine = create_async_engine(
    "postgresql+asyncpg://kurumaqq:1682@192.168.0.12/cloud",
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def validate_user(username: str, password: str):
    async with AsyncSessionLocal() as session:
        stm = select(User).where(User.username == username)    
        result =  await session.execute(stm)
        user = result.scalar_one_or_none()

        if not user:
            raise InvalidCredentialsHttpError()
        
        if not validate_password(password, user.password):
            raise InvalidCredentialsHttpError()
        return True

async def validate_user_dirs(request: Request, path):
    acces_token = request.cookies.get("ACCESS_TOKEN")
    decode_token = authx._decode_token(acces_token.encode())
    username = decode_token.username
    async with AsyncSessionLocal() as session:
        stm = select(User).where(User.username == username)
        path = Path(str(path).replace("\\", "/").strip()).resolve()
        result = await session.execute(stm)
        user = result.scalar_one_or_none()
        allowed_dirs = [Path(p).resolve() for p in user.owner_dirs.keys()]

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role == "admin": return True
        if not any(path == p or path.is_relative_to(p) for p in allowed_dirs):
            raise HTTPException(status_code=403, detail="Access denied")    

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
    decode_jwt = authx._decode_token(access_token)
    username = decode_jwt.username

    if access_token:
        try:
            payload = await authx.access_token_required(request)
            return payload
        except AuthXException:
            pass

    if refresh_token:
        try:
            data = {"username": username}
            payload = await authx.refresh_token_required(request)
            uid = payload.sub

            if response:
                new_access_token = authx.create_access_token(uid=uid, data=data)
                authx.set_access_cookies(
                    new_access_token,
                    response,
                    int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
                )

                new_refresh_token = authx.create_refresh_token(uid=uid, data=data)
                authx.set_refresh_cookies(
                    new_refresh_token,
                    response,
                    int(config_authx.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
                )

            return payload
        except AuthXException:
            raise HTTPException(status_code=401, detail="Session expired")

    raise HTTPException(status_code=401, detail="Not authenticated")
