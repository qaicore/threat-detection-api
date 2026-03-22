from multiprocessing import current_process
from fastapi import FastAPI, Depends
from fastapi import HTTPException
from database import engine
from models import Base, Case, User, Indicator
from schemas import UserCreate, UserResponse, IndicatorCreate, CaseCreate
from database import get_db
from auth import hash_password, verify_password, create_token, get_current_user
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
    
@app.post("/indicators")
def create_indicator(indicator: IndicatorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_indicator = Indicator(value = indicator.value, type = indicator.type, severity = indicator.severity, notes = indicator.notes, tags = indicator.tags )
    db.add(new_indicator)
    db.commit()
    db.refresh(new_indicator)
    return new_indicator

@app.get("/indicators")
def list_indicators(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    indicators = db.query(Indicator).all()
    return indicators

@app.get("/indicators/{id}")
def id_indicator(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    indicator = db.query(Indicator).filter(Indicator.id == id).first()
    return indicator

@app.post("/cases")
def create_case(case: CaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_case = Case(title = case.title, description = case.description, severity = case.severity)
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case

@app.get("/cases")
def list_cases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cases = db.query(Case).all()
    return cases

@app.get("/cases/{id}")
def id_case(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.id == id).first()
    return case