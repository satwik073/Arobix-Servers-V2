from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Database.database_settings import get_database_secure_connection
from Users.Models.user_model import User
from Users.Schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

@router.post("/user/creation", response_model=UserResponse, summary="Create a new user")
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_database_secure_connection)):
    # Check if user already exists
  

    # Create new user
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=user_in.password,
        role=user_in.role,
        account_status=user_in.account_status,
        phone_number=user_in.phone_number,
        preferences=user_in.preferences,
        language=user_in.language,
        timezone=user_in.timezone,
        subscription_plan=user_in.subscription_plan,
        created_by=user_in.created_by
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
