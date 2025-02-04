from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    JSON,
    UUID,
    ForeignKey,
    BigInteger,
    Enum,
    Integer,
    Index
)
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from Database.base_class import Base

class AutomationInstance(Base):
    __tablename__ = "automation_instances"

    # Basic Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    automation_id = Column(UUID(as_uuid=True), ForeignKey("automations.id", ondelete="CASCADE"), nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    miscdata = Column(JSON, default={})  # Flexible data storage for custom attributes

    # Additional Features
    external_reference = Column(String, nullable=True)  # External system reference for integration
    error_logs = Column(JSON, default=[])  # Stores error logs for debugging
    start_time = Column(DateTime, nullable=True)  # Track when automation started
    end_time = Column(DateTime, nullable=True)  # Track when automation ended
    status = Column(Enum("Pending", "InProgress", "Completed", "Failed", name="automation_instance_status_enum"), 
                    default="Pending", nullable=False)  # Status of the instance

    # Relationships
    automation = relationship("Automation", back_populates="automation_instances")

    # Additional Indexes
    __table_args__ = (
        Index("idx_automation_instance_automation_id", "automation_id"),
        Index("idx_automation_instance_active", "active"),
        Index("idx_automation_instance_status", "status"),
        Index("idx_automation_instance_created_at", "created_at"),
        Index("idx_automation_instance_external_reference", "external_reference"),
    )

