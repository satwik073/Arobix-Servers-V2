# from sqlalchemy.future import select
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import IntegrityError
# import logging
# import uuid
# from Database.database_settings import get_database_secure_connection
# from Users.Models.user_model import User
# from Users.Schemas.user_schema import UserCreate
# from Configs.configuration import Permissions, Role, SubscriptionTier, PrivacyLevel
# from Mapings.mapping_attributes import role_permissions
# from Organizations.Models.organization_model import Organization

# router = APIRouter()

# # Fetch default permissions based on role
# def get_default_permissions(role: str):
#     return role_permissions.get(role, role_permissions.get(Role.SUPER_ADMIN))

# @router.post("/user/creation", summary="Create a new user with an Organization if not provided")
# async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_database_secure_connection)):
#     try:
#         # Step 1: Check if user already exists
#         existing_user = await db.execute(select(User).filter(User.email == user_in.email))
#         if existing_user.scalars().first():
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

#         # Step 2: Handle Organization
#         organization_instance = None
        
#         if user_in.organization_id:  
#             # Fetch existing organization
#             organization_query = await db.execute(select(Organization).filter(Organization.id == user_in.organization_id))
#             organization_instance = organization_query.scalars().first()
#             if not organization_instance:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

#             # ✅ If agencies are provided, update the organization with new agencies
#             if user_in.agencies:
#                 organization_instance.agencies = user_in.agencies

#         else:
#             # Create a new organization if no organization ID was provided
#             new_organization = Organization(
#                 id=uuid.uuid4(),
#                 name=user_in.organization_name or f"{user_in.name}'s Organization",
#                 description="Default organization created with user",
#                 is_active=True,
#                 subscription_plan=SubscriptionTier.FREE,
#                 privacy_policy_url=None,
#                 terms_of_service_url=None,
#                 gdpr_compliance=False,
#                 two_factor_required=False,
#                 data_encryption_level=PrivacyLevel.CONFIDENTIAL,
#                 created_by=user_in.created_by,
#                 updated_by=user_in.created_by,
#                 agencies=user_in.agencies or []  # ✅ Store multiple agency IDs
#             )

#             db.add(new_organization)
#             await db.commit()
#             await db.refresh(new_organization)
#             organization_instance = new_organization  # ✅ Ensure ORM instance is used properly

#         # Step 3: Fetch default permissions for the SUPER_ADMIN role
#         user_role = Role.SUPER_ADMIN
#         default_permissions = get_default_permissions(user_role)

#         # ✅ Ensure permissions are stored as JSON/dictionary
#         if isinstance(default_permissions, str):
#             import json
#             default_permissions = json.loads(default_permissions)

#         # ✅ Ensure preferences are stored as JSON/dictionary
#         if isinstance(user_in.preferences, str):
#             import json
#             user_in.preferences = json.loads(user_in.preferences)

#         # ✅ Fix - Assign `organization_id`, not `organization_instance` directly
#         new_user = User(
#             name=user_in.name,
#             email=user_in.email,
#             hashed_password=user_in.password,  # Ensure password hashing in production
#             role=user_role,  
#             account_status=user_in.account_status,
#             phone_number=user_in.phone_number,
#             preferences=user_in.preferences,
#             language=user_in.language,
#             timezone=user_in.timezone,
#             subscription_plan=user_in.subscription_plan,
#             created_by=user_in.created_by,
#             organization_id=organization_instance.id,  # ✅ Assign UUID, not full object
#             permissions_by_authority=default_permissions  # ✅ Assign valid JSON/dictionary
#         )

#         db.add(new_user)
#         await db.commit()
#         await db.refresh(new_user)

#         return {
#             "user": new_user,
#             "organization": organization_instance
#         }

#     except IntegrityError:
#         await db.rollback()
#         logging.error("Database integrity error: Possible duplicate entry or constraint violation.")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database error: Duplicate entry detected")

#     except Exception as e:
#         await db.rollback()
#         logging.error(f"Unexpected error during user creation: {str(e)}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging
import uuid
from Database.database_settings import get_db
from Users.Models.user_model import User
from Users.Schemas.user_schema import UserCreate
from Configs.configuration import Role
from Mapings.mapping_attributes import role_permissions
from Organizations.Models.organization_model import Organization

router = APIRouter()

# ✅ Fetch default permissions based on role
def get_default_permissions(role: str):
    return role_permissions.get(role, role_permissions.get(Role.SUPER_ADMIN))

@router.post("/user/creation", summary="Create a new user with an Organization if not provided")
async def create_user(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)
):
    try:
        # Step 1: Check if user already exists
        async with db.begin():  # ✅ Ensures transaction safety
            existing_user_result = await db.execute(select(User).filter(User.email == user_in.email))
            existing_user = existing_user_result.scalars().first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )

            # Step 2: Handle Organization
            organization_instance = None
            if user_in.organization_id:
                organization_result = await db.execute(
                    select(Organization).filter(Organization.id == user_in.organization_id)
                )
                organization_instance = organization_result.scalars().first()

                if not organization_instance:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Organization not found"
                    )

            else:
                # Create a new organization if no organization ID was provided
                new_organization = Organization(
                    id=uuid.uuid4(),
                    name=user_in.organization_name or f"{user_in.name}'s Organization",
                    description="Default organization created with user",
                    is_active=True,
                    created_by=user_in.created_by,
                    updated_by=user_in.created_by,
                    agencies=user_in.agencies or []
                )
                db.add(new_organization)
                await db.flush()  # ✅ Ensures the new org ID is available
                organization_instance = new_organization

            # Step 3: Fetch default permissions for the SUPER_ADMIN role
            user_role = Role.SUPER_ADMIN
            default_permissions = get_default_permissions(user_role)

            # ✅ Ensure permissions & preferences are stored as JSON/dictionary
            if isinstance(default_permissions, str):
                import json
                default_permissions = json.loads(default_permissions)

            if isinstance(user_in.preferences, str):
                import json
                user_in.preferences = json.loads(user_in.preferences)

            # Step 4: Create a new user
            new_user = User(
                name=user_in.name,
                email=user_in.email,
                hashed_password=user_in.password,  # Ensure password hashing in production
                role=user_role,
                account_status=user_in.account_status,
                phone_number=user_in.phone_number,
                preferences=user_in.preferences,
                language=user_in.language,
                timezone=user_in.timezone,
                subscription_plan=user_in.subscription_plan,
                created_by=user_in.created_by,
                organization_id=organization_instance.id,
                permissions_by_authority=default_permissions
            )

            db.add(new_user)
            await db.flush()  # ✅ Ensures the user ID is available

            # ✅ Step 5: Update the organization to include the user in `user_ids`
            if organization_instance.user_ids is None:
                organization_instance.user_ids = {}

            organization_instance.user_ids[str(new_user.id)] = user_role.value

            await db.commit()  # ✅ Final commit after all updates

            return {
                "user": new_user,
                "organization": organization_instance
            }

    except IntegrityError:
        # await db.rollback()
        logging.error("Database integrity error: Possible duplicate entry or constraint violation.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error: Duplicate entry detected"
        )

    except Exception as e:
        # await db.rollback()
        logging.error(f"Unexpected error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
