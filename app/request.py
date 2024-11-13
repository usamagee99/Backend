from pydantic import BaseModel

class RequestData(BaseModel):
    body: str