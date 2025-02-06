import uuid
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Enum, Boolean, JSON, Index, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Configs.configuration import Role, PrivacyLevel
from Database.base_class import Base


class Permissions(Base):
    __tablename__ = 'permissions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False, index=True)
    subAccountId = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False, index=True)
    access = Column(Boolean, default=False, nullable=False)
    role_override = Column(Enum(Role), nullable=True)
    assigned_by = Column(UUID(as_uuid=True), nullable=True, index=True)
    assigned_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    permissions_type = Column(Enum("basic", "advanced", "custom", name="permissions_type_enum"), default="basic", nullable=False)
    restrictions = Column(JSON, default={"read_only": False, "api_rate_limit": None}, nullable=False)
    additional_miscdata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="permissions", lazy="joined")
    subAccount= relationship("SubAccount", back_populates="permissions", lazy="joined")

    # Indices
    __table_args__ = (
        Index("idx_email_sub_account", "email", "subAccountId"),
        Index("idx_permissions_type", "permissions_type"),
        Index("idx_assigned_by", "assigned_by"),
    )
