from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from ..database import Base


class DeviceData(Base):
    __tablename__ = "device_data"
    id = mapped_column(Integer, primary_key=True)
    device_id = mapped_column(ForeignKey("devices.id"))
    ttl = mapped_column(Integer)
    record_version = mapped_column(Integer)
    data_length = mapped_column(Integer)
    date = mapped_column(DateTime)
    device = relationship("Device", back_populates="device_data")
    data_readings = relationship("DataReading", back_populates="device_data")

class DeviceType(Base):
    __tablename__ = "device_types"
    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String(40), nullable=False)
    device = relationship("Device", back_populates="device_type")

class Device(Base):
    __tablename__ = "devices"
    id = mapped_column(Integer, primary_key=True)
    ip_address = mapped_column(String(45))
    is_active = mapped_column(Boolean, default=True)
    device_type_id = mapped_column(ForeignKey("device_types.id"))
    station_id = mapped_column(ForeignKey("stations.id"))
    device_type = relationship("DeviceType", back_populates="device")
    station = relationship("Station", back_populates="device")
    device_data = relationship("DeviceData", back_populates="device")

class Station(Base):
    __tablename__ = "stations"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False)
    city = mapped_column(String(200), nullable=False)
    device = relationship("Device", back_populates="station")
    station_user_mapping = relationship("UserStation", back_populates="station")

class UserStation(Base):
    __tablename__ = "user_stations"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    station_id = mapped_column(ForeignKey("stations.id"))
    user = relationship("User", back_populates="user_stations")
    station = relationship("Station", back_populates="station_user_mapping")

class DataReading(Base):
    __tablename__ = "data_readings"
    id = mapped_column(Integer, primary_key=True)
    device_data_id = mapped_column(ForeignKey("device_data.id"))
    value = mapped_column(Integer)
    device_data = relationship("DeviceData", back_populates="data_readings")

class UserType(Base):
    __tablename__ = "user_types"
    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String(40), nullable=False)
    user = relationship("User", back_populates="user_type")

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(45))
    last_name = mapped_column(String(45))
    password = mapped_column(String(500))
    phone = mapped_column(String(40))
    email = mapped_column(String(200))
    username = mapped_column(String(200))

    is_active = mapped_column(Boolean, default=True)
    user_type_id = mapped_column(ForeignKey("user_types.id"))
    user_type = relationship("UserType", back_populates="user")
    user_stations = relationship("UserStation", back_populates="user")