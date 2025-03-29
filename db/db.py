from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DTABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost/books'

engine = create_async_engine(DTABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)