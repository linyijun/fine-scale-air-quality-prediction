from sqlalchemy import Column, String, Float, Integer, Sequence, BigInteger
from geoalchemy2 import Geometry

from data_models.common_db import Base


class BufferTemplate(object):
    __table_args__ = {'schema': 'geographic_data'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    buffer_size = Column(Integer, nullable=False)
    buffer = Column(Geometry('POLYGON', srid=4326), nullable=False)


class LosAngelesEPA3000mBuffer(BufferTemplate, Base):
    __tablename__ = 'los_angeles_epa_3000m_buffer'


class LosAngelesFishnet3000mBuffer(BufferTemplate, Base):
    __tablename__ = 'los_angeles_fishnet_3000m_buffer'


