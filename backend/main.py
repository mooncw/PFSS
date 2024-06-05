from fastapi import FastAPI
from domain.sensor import sensor_router

app = FastAPI()

app.include_router(sensor_router.router)