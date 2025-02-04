from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Enum,
    JSON,
    BigInteger,
    Index
)
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
# from Configs.configuration import AutomationStatus
from Database.base_class import Base

class Automation(Base):
    __tablename__ = "automations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    trigger_id = Column(UUID(as_uuid=True), ForeignKey("triggers.id", ondelete="CASCADE"), nullable=True)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    status = Column(Enum("Active", "Inactive", "Archived", name="automation_status_enum"), default="Active", nullable=False)
    conditions = Column(JSON, default={})
    actions = Column(JSON, default={})
    miscdata = Column(JSON, default={})
    external_id = Column(BigInteger, unique=True, nullable=True)

    trigger = relationship("Trigger", back_populates="automations")
    sub_account = relationship("SubAccount", back_populates="automations")
    action_items = relationship("Action", back_populates="automation", cascade="all, delete-orphan")
    automation_instances = relationship("AutomationInstance", back_populates="automation", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_automation_sub_account_id", "sub_account_id"),
        Index("idx_automation_trigger_id", "trigger_id"),
        Index("idx_automation_status", "status"),
        Index("idx_automation_external_id", "external_id"),
        Index("idx_automation_published", "published"),
    )
