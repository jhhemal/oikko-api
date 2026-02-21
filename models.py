from sqlalchemy import Column, Integer, String, Text
from database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    owner_name = Column(String)
    phone = Column(String)
    city = Column(String)
    address = Column(String)
    description = Column(Text)