from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Sensor

router = APIRouter(
    prefix="/api/v1/sensors",
)

@router.get("/code")
def find_all_sensor_codes(db: Session = Depends(get_db)):
    _sensor_list = db.query(Sensor).all()
    return _sensor_list