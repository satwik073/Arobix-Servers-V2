from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from typing import Optional, Dict, List
from datetime import datetime
from Configs.configuration import Role, AccountStatus, LanguagePreference, SubscriptionTier


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=128)
    role: Role = Field(default=Role.SUBACCOUNT_USER)
    account_status: AccountStatus = Field(default=AccountStatus.ACTIVE)
    phone_number: Optional[str] = Field(None)
    preferences: Optional[Dict[str, str]] = Field(default={})
    language: LanguagePreference = Field(default=LanguagePreference.ENGLISH)
    timezone: str = Field(default="UTC")
    subscription_plan: SubscriptionTier = Field(default=SubscriptionTier.FREE)
    created_by: Optional[UUID] = Field(None)
    updated_by: Optional[UUID] = Field(None)


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
