"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    title: str
    prompt: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    title: str
    prompt: Optional[str]
    status: str
    output_video_key: Optional[str]

    class Config:
        orm_mode = True


class AssetCreate(BaseModel):
    project_id: int
    s3_key: str
    media_type: Optional[str]


class AssetOut(BaseModel):
    id: int
    s3_key: str
    media_type: Optional[str]
    metadata: Optional[str]

    class Config:
        orm_mode = True


class JobOut(BaseModel):
    id: int
    project_id: int
    status: str
    output_key: Optional[str]
    error: Optional[str]

    class Config:
        orm_mode = True
