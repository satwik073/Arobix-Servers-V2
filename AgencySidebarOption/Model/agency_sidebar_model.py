from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index, Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from Database.base_class import Base

class AgencySidebarOption(Base):
    __tablename__ = "agency_sidebar_options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, default="Menu", nullable=False)
    link = Column(String, default="#", nullable=False)
    icon = Column(String, default="info", nullable=False)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    agency = relationship("Agency", back_populates="sidebar_options")

    __table_args__ = (
        Index("idx_agency_sidebar_option_agency_id", "agency_id"),
    )
