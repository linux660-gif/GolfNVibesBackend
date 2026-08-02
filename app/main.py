from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import payments



app = FastAPI()

origins =[
    "http://localhost",
    "http://localhost:5173",
    "https://golfnvibes.co.ke",
    "https://golf-n-vibes-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    payments.router,
    prefix="/payments",
    tags=["Payments"]
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}







