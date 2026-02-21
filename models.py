# models.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    owner_name = Column(String)
    phone = Column(String)
    city = Column(String)
    address = Column(String)
    description = Column(String)