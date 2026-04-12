import ssl as ssl_module

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Supabase는 SSL 필수
connect_args = {}
if "supabase.com" in settings.DATABASE_URL:
    ssl_context = ssl_module.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl_module.CERT_NONE
    connect_args["ssl"] = ssl_context

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
