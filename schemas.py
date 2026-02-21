from pydantic import BaseModel
from typing import Optional

class BusinessCreate(BaseModel):
    name: str
    category: str
    owner_name: str
    phone: str
    city: str
    address: str
    description: Optional[str] = None

class BusinessUpdate(BusinessCreate):
    pass

class BusinessResponse(BusinessCreate):
    id: int

    class Config:
        from_attributes = True