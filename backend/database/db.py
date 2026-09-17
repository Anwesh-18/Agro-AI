import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL : str = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_async_engine(
    DATABASE_URL,
    echo = False,            # tells it not to print the sql queries in my terminal
    pool_pre_ping=True,      # Check for the connection each time before communicating
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()