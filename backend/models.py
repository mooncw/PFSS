from sqlalchemy import Column, Integer, String

from database import Base

class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)