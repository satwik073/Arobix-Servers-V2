from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index, Integer, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from Database.base_class import Base
class AddOns(Base):
    __tablename__ = "add_ons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    price_id = Column(String, unique=True, nullable=False)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    agency = relationship("Agency", back_populates="add_ons")

    __table_args__ = (
        Index("idx_add_on_agency_id", "agency_id"),
    )
