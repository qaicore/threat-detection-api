from multiprocessing import current_process
from fastapi import FastAPI, Depends
from fastapi import HTTPException
from database import engine
from models import Base, Case, User, Indicator, CaseIndicator
from schemas import UserCreate, UserResponse, IndicatorCreate, IndicatorResponse, CaseCreate, CaseResponse, CaseStatusUpdate, CaseIndicatorCreate
from database import get_db
from auth import hash_password, verify_password, create_token, get_current_user
from sqlalchemy.orm import Session


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
    
@app.post("/api/indicators", status_code=201, response_model=IndicatorResponse)
def create_indicator(indicator: IndicatorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_indicator = Indicator(value = indicator.value, type = indicator.type, severity = indicator.severity, notes = indicator.notes, tags = indicator.tags, submitted_by = current_user.id)
    db.add(new_indicator)
    db.commit()
    db.refresh(new_indicator)
    return new_indicator

@app.get("/api/indicators", response_model=list[IndicatorResponse])
def list_indicators(
    skip: int = 0,
    limit: int = 20,
    type: str = None,
    severity: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Indicator)
    if type:
        query = query.filter(Indicator.type == type)
    if severity:
        query = query.filter(Indicator.severity == severity)
    return query.offset(skip).limit(limit).all()

@app.get("/api/indicators/{id}", response_model=IndicatorResponse)
def id_indicator(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    indicator = db.query(Indicator).filter(Indicator.id == id).first()
    if indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return indicator
    

@app.post("/api/cases", status_code=201, response_model=CaseResponse)
def create_case(case: CaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_case = Case(title = case.title, description = case.description, severity = case.severity)
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case

@app.get("/api/cases", response_model=list[CaseResponse])
def list_cases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cases = db.query(Case).all()
    return cases

@app.get("/api/cases/{id}", response_model=CaseResponse)
def id_case(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.id == id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
    

@app.patch("/api/cases/{id}/status", response_model=CaseResponse)
def update_case(id: int, status_update: CaseStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.id == id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    case.status = status_update.status
    db.commit()
    db.refresh(case)
    return case
   
@app.post("/api/cases/{id}/indicators")
def case_indicators(case_indicator: CaseIndicatorCreate, id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.id == id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    indicator = db.query(Indicator).filter(Indicator.id == case_indicator.indicator_id).first()
    if indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    new_case_indicator = CaseIndicator(case_id = id, indicator_id = case_indicator.indicator_id)
    db.add(new_case_indicator)
    db.commit()
    db.refresh(new_case_indicator)
    return new_case_indicator