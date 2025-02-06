from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import logging
from Database.database_settings import get_database_secure_connection
from Users.Models.user_model import User
from Users.Schemas.user_schema import UserCreate, UserResponse

router = APIRouter()



@router.post("/user/creation",summary="Create a new user")
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_database_secure_connection)):
    try:
        existing_user = await db.execute(User.__table__.select().where(User.email == user_in.email))
        if existing_user.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

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

    except IntegrityError:
        await db.rollback()
        logging.error("Database integrity error: Possible duplicate entry or constraint violation.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database error: Duplicate entry detected")

    except Exception as e:
        await db.rollback()
        logging.error(f"Unexpected error during user creation: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
