from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index, Integer, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from Database.base_class import Base

class Invitation(Base):
    __tablename__ = "invitations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String, unique=True, nullable=False)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum("PENDING", "ACCEPTED", "REJECTED", name="invitation_status_enum"), default="PENDING", nullable=False)
    role = Column(Enum("SUBACCOUNT_USER", "AGENCY_USER", name="invitation_role_enum"), default="SUBACCOUNT_USER", nullable=False)

    # Relationships
    agency = relationship("Agency", back_populates="invitations")

    __table_args__ = (
        Index("idx_invitation_agency_id", "agency_id"),
    )
