from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Enum,
    JSON,
    Integer,
    ForeignKey,
    UUID,
    BigInteger,
    Index
)
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from Database.base_class import Base

class Action(Base):
    __tablename__ = "actions"

    # Basic Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum("ActionType1", "ActionType2", "ActionType3", name="action_types_enum"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    automation_id = Column(UUID(as_uuid=True), ForeignKey("automations.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    lane_id = Column(String, default="0", nullable=False)
    status = Column(Enum("Pending", "Completed", "Failed", "InProgress", name="action_status_enum"), default="Pending", nullable=False)
    parameters = Column(JSON, default={})  # Store dynamic parameters for complex actions

    # Additional Features
    external_data = Column(JSON, default={})  # External data for integration with third-party systems
    retries = Column(Integer, default=0)  # Track the number of retry attempts for failed actions
    max_retries = Column(Integer, default=3)  # Max retries allowed for a specific action
    estimated_duration = Column(Integer, nullable=True)  # Estimate of how long the action should take
    retry_delay = Column(Integer, nullable=True)  # Time delay (in seconds) between retry attempts

    # Relationships
    automation = relationship("Automation", back_populates="action_items")

    # Additional Indexes
    __table_args__ = (
        Index("idx_action_automation_id", "automation_id"),
        Index("idx_action_order", "order"),
        Index("idx_action_lane_id", "lane_id"),
        Index("idx_action_status", "status"),
        Index("idx_action_created_at", "created_at"),
        Index("idx_action_retries", "retries"),  # Index for retry attempts for quicker query filtering
        Index("idx_action_estimated_duration", "estimated_duration"),  # Index for quicker query based on estimated time
    )
