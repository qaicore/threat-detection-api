from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

class IndicatorCreate(BaseModel):
    type: str
    value: str
    severity: str
    notes: str = None
    tags: str = None

class IndicatorResponse(BaseModel):
    id: int
    submitted_by: int
    created_at: datetime
    type: str
    value: str
    severity: str
    notes: str = None
    tags: str = None

class CaseCreate(BaseModel):
    title: str
    description: str
    severity: str

class CaseResponse(BaseModel):
    title: str
    description: str
    severity: str
    status: str
    id: int
    assigned_to: int
    created_at: datetime
    updated_at: datetime