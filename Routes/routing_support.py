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
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from Database.database_settings import users_collection, organizations_collection
from Users.Schemas.user_schema import UserCreate
import logging
from Configs.configuration import Role
from Delta.Meta.queries import get_default_permissions

router = APIRouter()

@router.post("/user/creation", summary="Create a new user with an Organization if not provided")
async def create_user(user_in: UserCreate):
    try:
        # Step 1: Check if user already exists
        existing_user = await users_collection.find_one({"email": user_in.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Step 2: Handle Organization
        organization_instance = None
        organization_id = None

        if user_in.organization_id:
            organization_instance = await organizations_collection.find_one({"_id": user_in.organization_id})
            if not organization_instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Organization not found"
                )
            organization_id = organization_instance["_id"]
        else:
            # Ensure Enums are converted properly
            subscription_plan = (
                user_in.subscription_plan.value if hasattr(user_in.subscription_plan, "value") else user_in.subscription_plan
            )
            data_encryption_level = (
                user_in.data_encryption_level.value if hasattr(user_in.data_encryption_level, "value") else user_in.data_encryption_level
            )

            # Create a new organization with an empty user mapping
            new_organization = {
                "_id": str(ObjectId()),
                "name": user_in.organization_name or f"{user_in.name}'s Organization",
                "description": "Default organization created with user",
                "is_active": True,
                "subscription_plan": subscription_plan,
                "privacy_policy_url": None,
                "terms_of_service_url": None,
                "gdpr_compliance": False,
                "two_factor_required": False,
                "data_encryption_level": data_encryption_level,
                "created_by": user_in.created_by,
                "updated_by": user_in.created_by,
                "agencies": user_in.agencies or [],
                "user_ids": {}  # ✅ Initialize an empty dictionary for user-role mapping
            }

            # Insert new organization and fetch its ID
            insert_result = await organizations_collection.insert_one(new_organization)
            organization_id = str(insert_result.inserted_id)
            organization_instance = new_organization

        # Step 3: Fetch default permissions for the SUPER_ADMIN role
        user_role = Role.AGENCY_OWNER
        default_permissions = get_default_permissions(user_role)

        # Ensure permissions are stored as JSON/dictionary
        if isinstance(default_permissions, str):
            import json
            default_permissions = json.loads(default_permissions)

        # Ensure preferences are stored as JSON/dictionary
        if isinstance(user_in.preferences, str):
            import json
            user_in.preferences = json.loads(user_in.preferences)

        # Ensure role is converted correctly
        user_role_value = user_role.value if hasattr(user_role, "value") else user_role

        # Generate a new user ID
        new_user_id = str(ObjectId())

        # Create a new user
        new_user = {
            "_id": new_user_id,
            "name": user_in.name,
            "email": user_in.email,
            "hashed_password": user_in.password,  # Ensure password hashing in production
            "role": user_role_value,
            "account_status": user_in.account_status,
            "phone_number": user_in.phone_number,
            "preferences": user_in.preferences,
            "language": user_in.language,
            "timezone": user_in.timezone,
            "subscription_plan": subscription_plan,
            "created_by": user_in.created_by,
            "organization_id": organization_id,  # Assign only the ID
            "permissions_by_authority": default_permissions
        }

        # Insert the new user
        await users_collection.insert_one(new_user)

        # ✅ Step 4: Update the Organization to include this new user in `user_ids` with role as value
        await organizations_collection.update_one(
            {"_id": organization_id},
            {"$set": {f"user_ids.{new_user_id}": user_role_value}}
        )

        return {"user": new_user, "organization": organization_instance}

    except Exception as e:
        logging.error(f"Unexpected error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
