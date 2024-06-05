from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/sensors",
)

@router.get("/{sensor_id}")
def find_sensor(sensor_id: int):
    return

@router.get("/")
def find_all_sensors():
    return

@router.get("/id")
def find_all_sensor_id():
    return

@router.post("/")
def create_sensor():
    return

@router.delete("/{sensor_id}")
def delete_sensor(sensor_id):
    return