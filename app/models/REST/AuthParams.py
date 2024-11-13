from typing import Optional
from pydantic import BaseModel
from datetime import datetime, time, timedelta

class AuthParams(BaseModel):
    user_login: str
    password: str