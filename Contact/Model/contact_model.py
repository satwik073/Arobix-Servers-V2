from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from Database.base_class import Base

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    miscdata = Column(JSON, default={})  # Flexible miscdata field for additional contact data
    is_active = Column(Boolean, default=True)  # Field for contact activity status

    # Relationships
    subAccount = relationship("SubAccount", back_populates="contacts")
    tickets = relationship("Ticket", back_populates="contact", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_contact_sub_account_id", "sub_account_id"),
        Index("idx_contact_is_active", "is_active"),
    )
