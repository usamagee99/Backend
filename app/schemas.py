from pydantic import BaseModel
from datetime import datetime, time, timedelta

class DeviceDataBase(BaseModel):
    id: int
    data_fields: str | None = None
    date: datetime