from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    time = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
