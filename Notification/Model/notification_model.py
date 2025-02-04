from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index, Integer, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from Database.base_class import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    notification = Column(String, nullable=False)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    agency = relationship("Agency", back_populates="notifications")
    sub_account = relationship("SubAccount", back_populates="notifications")
    user = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("idx_notification_agency_id", "agency_id"),
        Index("idx_notification_user_id", "user_id"),
    )
