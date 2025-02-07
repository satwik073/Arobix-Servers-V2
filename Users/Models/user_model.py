import uuid
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Enum, Boolean, JSON, Index, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Configs.configuration import AccountStatus, LanguagePreference, PrivacyLevel, Role, SubscriptionTier
from Database.base_class import Base
from Delta.sub_account_user_association import sub_account_user_association


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    avatarUrl = Column(String, nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.SUBACCOUNT_USER, nullable=False)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0, nullable=False)
    two_factor_secret = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
    oauth_providers = Column(JSON, default={})
    password_history = Column(JSON, default=[])
    preferences = Column(JSON, default={})
    language = Column(Enum(LanguagePreference), default=LanguagePreference.ENGLISH, nullable=False)
    timezone = Column(String, default="IST")
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    agencyId = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    privacy_level = Column(Enum(PrivacyLevel), default=PrivacyLevel.INTERNAL, nullable=False)
    subscription_plan = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    subscription_expiry = Column(DateTime, nullable=True)
    notification_preferences = Column(JSON, default={"email": True, "sms": False, "push": True, "in_app": True})
    assigned_tickets = relationship("Ticket", back_populates="assigned_user", cascade="all, delete-orphan")
    subAccounts = relationship(
        "SubAccount",
        back_populates="subAccountTeamMembers",
        secondary=sub_account_user_association
    )
    permissions_by_authority = Column(JSON)
    organization = relationship("Organization", back_populates="users")
    agency = relationship("Agency", back_populates="Users")
    password_history = relationship("PasswordHistory", back_populates="user", cascade="all, delete-orphan")
    Ticket = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    permissions = relationship("Permissions", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_email", "email"),
        Index("idx_account_status", "account_status"),
        Index("idx_subscription_plan", "subscription_plan"),
        Index("idx_tenant_id", "tenant_id"),
    )
