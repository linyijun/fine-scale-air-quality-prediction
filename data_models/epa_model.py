from sqlalchemy import Column, BigInteger, Integer, String, Float, DateTime, Text, REAL, Sequence
from geoalchemy2 import Geometry

from data_models.common_db import Base


class LosAngelesEPATemplate(object):
    __table_args__ = {'schema': 'air_quality_data'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    station_id = Column(Integer, nullable=False)
    date_observed = Column(DateTime, nullable=False)
    parameter_name = Column(String(10), nullable=False)
    concentration = Column(REAL, nullable=False)
    unit = Column(Text)
    aqi = Column(REAL, nullable=False)
    category_number = Column(Integer)


class LosAngelesEPA2018(LosAngelesEPATemplate, Base):
    __tablename__='los_angeles_epa_air_quality_2018'


class LosAngelesEPA2019(LosAngelesEPATemplate, Base):
    __tablename__='los_angeles_epa_air_quality_2019'


class LosAngelesEPA2020(LosAngelesEPATemplate, Base):
    __tablename__='los_angeles_epa_air_quality_2020'

