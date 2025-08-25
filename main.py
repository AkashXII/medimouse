from fastapi import FastAPI, Depends, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import sessionLocal, engine, Base
from models import User, Medicine
from schemas import UserCreate, UserResponse, MedicineCreate
from passlib.context import CryptContext
from typing import List
from pydantic import BaseModel
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password): return pwd_context.hash(password)
def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)

# DB session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# Serve index.html at root
@app.get("/")
def root():
    return FileResponse("index.html")

# Login model
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": user.username}

# Create user
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        name=user.name,
        age=user.age,
        weight=user.weight,
        height=user.height,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# CRUD for medicines
@app.post("/medicines", response_model=MedicineCreate)
def create_medicine(med: MedicineCreate, username: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    new_med = Medicine(name=med.name, dosage=med.dosage, time=med.time, user_id=user.id)
    db.add(new_med)
    db.commit()
    db.refresh(new_med)
    return new_med

@app.get("/medicines/{username}", response_model=List[MedicineCreate])
def get_medicines(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return db.query(Medicine).filter(Medicine.user_id == user.id).all()

@app.delete("/medicines/{med_id}")
def delete_medicine(med_id: int, db: Session = Depends(get_db)):
    med = db.query(Medicine).filter(Medicine.id == med_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    db.delete(med)
    db.commit()
    return {"detail": "Medicine deleted"}

class MedicineUpdate(BaseModel):
    name: str
    dosage: str
    time: str

@app.put("/medicines/{med_id}", response_model=MedicineUpdate)
def update_medicine(med_id: int, med: MedicineUpdate, db: Session = Depends(get_db)):
    db_med = db.query(Medicine).filter(Medicine.id == med_id).first()
    if not db_med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    db_med.name = med.name
    db_med.dosage = med.dosage
    db_med.time = med.time
    db.commit()
    db.refresh(db_med)
    return db_med

# BMI route
@app.get("/users/{username}/bmi")
def get_bmi(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    if not user.height or not user.weight:
        return {"bmi": None, "message": "Height or weight not set"}
    bmi = user.weight / (user.height ** 2)
    category = ""
    if bmi < 18.5: category = "Underweight"
    elif bmi < 25: category = "Normal"
    elif bmi < 30: category = "Overweight"
    else: category = "Obese"
    return {"bmi": round(bmi,2), "category": category}
