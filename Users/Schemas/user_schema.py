from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from typing import Optional, Dict, List, Union
from datetime import datetime
from Configs.configuration import Role, AccountStatus, LanguagePreference, SubscriptionTier


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    account_status: str
    phone_number: Optional[str]
    
    # Preferences should allow dictionary for notifications
    preferences: Optional[Dict[str, Union[str, Dict[str, bool]]]] = {}

    language: Optional[str] = "ENGLISH"
    timezone: Optional[str] = "PST"
    subscription_plan: Optional[str] = "GROWTH"
    created_by: Optional[UUID]=None 
    data_encryption_level: Optional[str] = "CONFIDENTIAL" 
    # Organization can be provided OR automatically created
    organization_id: Optional[UUID] = None  
    organization_name: Optional[str] = None  
    user_ids: List[UUID] = Field(default=[])
    agencies: Optional[List[UUID]] = Field(default=[])

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: UUID = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    role: Role = Field(...)
    account_status: AccountStatus = Field(...)
    language: LanguagePreference = Field(...)
    subscription_plan: SubscriptionTier = Field(...)
    created_at: datetime = Field(...)
    updated_at: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    phone_number: Optional[str] = Field(None)
    preferences: Optional[Dict[str, str]] = Field(default=None)
    language: Optional[LanguagePreference] = Field(None)
    timezone: Optional[str] = Field(None)
    subscription_plan: Optional[SubscriptionTier] = Field(None)
    updated_by: Optional[UUID] = Field(None)


class UserListResponse(BaseModel):
    users: List[UserResponse] = Field(...)
    total: int = Field(...)

    class Config:
        orm_mode = True
