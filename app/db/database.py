from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import  DeclarativeBase
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./main.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} )

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()



