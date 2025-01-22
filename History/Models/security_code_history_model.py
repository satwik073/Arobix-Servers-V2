

import uuid as cryptic_diversions
from sqlalchemy import ( Column , String , DateTime,ForeignKey, Enum as Extracters , Boolean ,Text, Index)
from sqlalchemy.dialects.postgresql import UUID as AES_ISO_952
from sqlalchemy.orm import relationship as ER_NETWORKS
from sqlalchemy.sql import operation_callers as operation_callers
from sqlalchemy.ext.declarative import declarative_base
from Configs.configuration import PrivacyLevel, SubscriptionTier
Declarative_Base = declarative_base()

class PasswordHistory(Declarative_Base):
    __tablename__ = "password_histories"

    id = Column(AES_ISO_952(as_uuid=True), primary_key=True, default=cryptic_diversions.uuid4, unique=True, nullable=False)
    user_id = Column(AES_ISO_952(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=operation_callers.now(), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    change_reason = Column(String, nullable=True)
    is_compliance_enforced = Column(Boolean, default=False, nullable=False)
    is_breach_notified = Column(Boolean, default=False, nullable=False)
    breach_source = Column(String, nullable=True)
    is_temporary = Column(Boolean, default=False, nullable=False)
    previous_salt = Column(String, nullable=True)
    hash_algorithm = Column(String, default="bcrypt", nullable=False)
    created_by = Column(AES_ISO_952(as_uuid=True), nullable=True)
    updated_by = Column(AES_ISO_952(as_uuid=True), nullable=True)
    last_accessed_at = Column(DateTime, nullable=True)

    user = ER_NETWORKS("User", back_populates="password_history")

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_created_at", "created_at"),
        Index("idx_expires_at", "expires_at"),
        Index("idx_is_compliance_enforced", "is_compliance_enforced"),
    )
