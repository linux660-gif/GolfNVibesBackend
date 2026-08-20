from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import  newsletter, trip, members, email
from app.db.database import Base, engine
from app.core.logging_config import setup_logging


setup_logging()

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
app = FastAPI(lifespan=lifespan)

origins =[
    "http://localhost",
    "http://localhost:5173",
    "https://golfnvibes.com",
    "https://golf-n-vibes-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#app.include_router(payments.router)
app.include_router(trip.router)
app.include_router(newsletter.router)
app.include_router(members.router)
app.include_router(email.router)
@app.get("/")
async def root():
    return {"message": "Hello, World!"}







