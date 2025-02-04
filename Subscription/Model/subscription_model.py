from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index, Integer, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from Database.base_class import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    plan = Column(String, nullable=True)
    price = Column(String, nullable=True)
    active = Column(Boolean, default=False)
    price_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    current_period_end_date = Column(DateTime, nullable=False)
    subscription_id = Column(String, unique=True, nullable=False)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    agency = relationship("Agency", back_populates="subscriptions")

    __table_args__ = (
        Index("idx_subscription_customer_id", "customer_id"),
        Index("idx_subscription_agency_id", "agency_id"),
    )
