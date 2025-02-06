from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from Database.base_class import Base

class Funnel(Base):
    __tablename__ = "funnels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    description = Column(String, nullable=True)
    published = Column(Boolean, default=False, nullable=False)
    sub_domain_name = Column(String, unique=True, nullable=True)
    favicon = Column(String, nullable=True)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    live_products = Column(String, default="[]", nullable=False)  # Store list of products in JSON format

    # Relationships
    subAccount= relationship("SubAccount", back_populates="funnels")
    funnel_pages = relationship("FunnelPage", back_populates="funnel", cascade="all, delete-orphan")
    class_names = relationship("ClassName", back_populates="funnel", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_funnel_sub_account_id", "sub_account_id"),
        Index("idx_funnel_live_products", "live_products"),
    )
