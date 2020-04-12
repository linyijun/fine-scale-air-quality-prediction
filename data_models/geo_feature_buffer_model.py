from sqlalchemy import Column, Integer, String, Text, Float, BigInteger

from data_models.common_db import Base


class GeoFeatureTemplate(object):
    __table_args__ = {'schema': 'geographic_data'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=True)
    geo_feature = Column(Text, nullable=True)
    feature_type = Column(String(20), nullable=True)
    buffer_size = Column(Integer, nullable=True)
    value = Column(Float(53), nullable=True)
    measurement = Column(Text, nullable=True)


class LosAngelesEpaGeoFeature(GeoFeatureTemplate, Base):
    __tablename__ = 'los_angeles_epa_geo_feature'


class LosAngelesFishnetGeoFeature(GeoFeatureTemplate, Base):
    __tablename__ = 'los_angeles_fishnet_geo_feature'
