from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    JSON,
    Boolean,
    BigInteger,
    Index
)
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
# from Configs.configuration import TriggerTypes
from Database.base_class import Base

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(Enum("Time", "Event", "Manual", name="trigger_type_enum"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    miscdata = Column(JSON, default={})
    is_active = Column(Boolean, default=True, nullable=False)
    external_reference_id = Column(BigInteger, unique=True, nullable=True)


    subAccount = relationship("SubAccount", back_populates="triggers")
    automations = relationship("Automation", back_populates="trigger", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_trigger_sub_account_id", "sub_account_id"),
        Index("idx_trigger_type", "type"),
        Index("idx_trigger_is_active", "is_active"),
        Index("idx_trigger_external_reference_id", "external_reference_id"),
    )
