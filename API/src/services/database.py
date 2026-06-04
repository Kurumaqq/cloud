from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.model import User
from sqlalchemy import select
from src.errors.login import InvalidCredentialsHttpError

engine = create_async_engine(
    "postgresql+asyncpg://kurumaqq:1682@192.168.0.12/cloud",
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_user(username: str):
    async with AsyncSessionLocal() as session:
        stm = select(User).where(User.username == username)
        result = await session.execute(stm)
        user = result.scalar_one_or_none()

        if not user:
            raise InvalidCredentialsHttpError()
        
        return user
