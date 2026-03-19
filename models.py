
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="ANALYST")
    created_at = Column(DateTime, default=datetime.utcnow)

class Indicator(Base):
    __tablename__ = "indicators"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    value = Column(String, unique=True, nullable=False)
    severity = Column(String, nullable=False)
    tags = Column(String,)
    notes = Column(String,)
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CaseIndicator(Base):
    __tablename__ = "case_indicators"
    case_id = Column(Integer, ForeignKey("cases.id"), primary_key=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), primary_key=True)