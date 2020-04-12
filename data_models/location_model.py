from sqlalchemy import Column, String, Float, Integer, Sequence, BigInteger
from geoalchemy2 import Geometry

from data_models.common_db import Base


class LosAngelesFishnet(Base):
    __table_args__ = {'schema': 'geographic_data'}
    __tablename__ = 'los_angeles_fishnet'

    gid = Column(Integer, primary_key=True)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)


class LosAngelesEPASensorLocations(Base):
    __table_args__ = {'schema': 'air_quality_data'}
    __tablename__ = 'los_angeles_epa_sensor_locations'

    station_id = Column(Integer, primary_key=True)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    elevation = Column(Float(53), nullable=False)

