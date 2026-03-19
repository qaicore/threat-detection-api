from fastapi import FastAPI, Depends
from fastapi import HTTPException
from database import engine
from models import Base, User
from schemas import UserCreate, UserResponse
from database import get_db
from auth import hash_password, verify_password, create_token
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="Password too long")
    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed,role="ANALYST")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    verify_user = verify_password(user.password, existing_user.hashed_password)
    if not verify_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_token = create_token({"sub": existing_user.email})
    return user_token
    
   