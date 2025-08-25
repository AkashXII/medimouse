from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    name: str
    age: int
    weight: float
    height: float

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class MedicineCreate(BaseModel):
    name: str
    dosage: str
    time: str

class MedicineResponse(MedicineCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True
