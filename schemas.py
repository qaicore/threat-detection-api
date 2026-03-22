from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    submitted_by: Optional[int] = None
    created_at: datetime
    type: str
    value: str
    severity: str
    notes: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        from_attributes = True

class CaseCreate(BaseModel):
    title: str
    description: str
    severity: str

class CaseResponse(BaseModel):
    from_attributes = True
    title: str
    description: str
    severity: str
    status: str
    id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CaseStatusUpdate(BaseModel):
    status: str

class CaseIndicatorCreate(BaseModel):
    indicator_id: int