import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Enum,
    Float,
    JSON,
    Boolean,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Configs.configuration import SubscriptionTier
from Database.base_class import Base


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    subAccountId = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum("Active", "Inactive", "Archived", name="pipeline_status_enum"), default="Active", nullable=False)
    priority = Column(Enum("Low", "Medium", "High", name="pipeline_priority_enum"), default="Medium", nullable=False)
    privacy_level = Column(Enum("Public", "Private", "Restricted", name="pipeline_privacy_level_enum"), default="Private", nullable=False)
    estimated_value = Column(Float, default=0.0, nullable=True)
    goal = Column(Integer, default=5, nullable=False)
    metrics = Column(JSON, default={}, nullable=True)
    integrations = Column(JSON, default={}, nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)

    subAccount = relationship("SubAccount", back_populates="pipelines", cascade="all, delete-orphan")
    lanes = relationship("Lane", back_populates="pipeline", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="pipeline_tags", back_populates="pipelines")

    __table_args__ = (
        Index("idx_sub_account_id", "subAccountId"),
        Index("idx_status", "status"),
        Index("idx_priority", "priority"),
        Index("idx_is_public", "is_public"),
    )
