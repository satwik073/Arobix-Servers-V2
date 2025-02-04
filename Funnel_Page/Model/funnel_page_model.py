from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index, Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from Database.base_class import Base

class FunnelPage(Base):
    __tablename__ = "funnel_pages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    path_name = Column(String, default="")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    visits = Column(Integer, default=0)
    content = Column(String, nullable=True)
    order = Column(Integer, nullable=False)
    preview_image = Column(String, nullable=True)
    funnel_id = Column(UUID(as_uuid=True), ForeignKey("funnels.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    funnel = relationship("Funnel", back_populates="funnel_pages")

    __table_args__ = (
        Index("idx_funnel_page_funnel_id", "funnel_id"),
    )
