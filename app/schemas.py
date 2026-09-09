from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class VaultEntryCreate(BaseModel):
    site_name: str
    site_url: Optional[str] = None
    login: str
    password: str

class VaultEntryResponse(BaseModel):
    id: int
    site_name: str
    site_url: Optional[str] = None
    login: str
    created_at: datetime

    class Config:
        from_attributes = True