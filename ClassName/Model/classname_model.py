from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from Database.base_class import Base

class ClassName(Base):
    __tablename__ = "class_names"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    funnel_id = Column(UUID(as_uuid=True), ForeignKey("funnels.id", ondelete="CASCADE"), nullable=False)
    custom_data = Column(JSON, default={})  # Flexible field to store custom class-specific data

    # Relationships
    funnel = relationship("Funnel", back_populates="class_names")

    __table_args__ = (
        Index("idx_class_name_funnel_id", "funnel_id"),
    )
