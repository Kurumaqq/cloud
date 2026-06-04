from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.model import User
from sqlalchemy import select
from src.errors.login import InvalidCredentialsHttpError
from fastapi import Request
from src.config import authx

engine = create_async_engine(
    "postgresql+asyncpg://kurumaqq:1682@192.168.0.12/cloud",
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_user(user_or_request: str) -> User:
    if isinstance(user_or_request, Request):
        acces_token = user_or_request.cookies.get("ACCESS_TOKEN")
        decode_token = authx._decode_token(acces_token.encode())
        username = decode_token.username
    else:
        username = user_or_request
    async with AsyncSessionLocal() as session:
        stm = select(User).where(User.username == username)
        result = await session.execute(stm)
        user = result.scalar_one_or_none()

        if not user:
            raise InvalidCredentialsHttpError()

        return user


async def get_rights(user_or_request: str | Request) -> User:
    if isinstance(username, Request):
        acces_token = user_or_request.cookies.get("ACCESS_TOKEN")
        decode_token = authx._decode_token(acces_token.encode())
        username = decode_token.username
    else: username = user_or_request
    user = await get_user(username)
    print(user.rights)
    return user.rights
