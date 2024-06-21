from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from domain.sensor import sensor_router

app = FastAPI()

# CORS 설정
origins = [
    # "http://localhost",
    "http://localhost:3000",  # React 애플리케이션의 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(sensor_router.router)