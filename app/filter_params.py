from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta

class FilterParams(BaseModel):
    items_per_page: int = 40
    page: int = 1
    operator_id: int | None = Field(default=None, nullable=True) # Optional[int] = None
    vehicle_no: Optional[int] = None
    device_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None