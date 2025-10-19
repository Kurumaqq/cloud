from sqlalchemy import String 
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(80))
    role: Mapped[str] = mapped_column(String(30), default="user")
    owner_dirs: Mapped[dict[str, int]] = mapped_column(JSONB, default={})
