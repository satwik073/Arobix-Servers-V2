from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Enum,
    JSON,
    Boolean,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.sql import func
from Database.base_class import Base


class Lane(Base):
    __tablename__ = "lanes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    pipelineId = Column(UUID(as_uuid=True), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, default=0, nullable=False)
    status = Column(Enum("Active", "Inactive", "Archived", name="lane_status"), default="Active", nullable=False)
    goal = Column(Integer, default=5, nullable=False)
    metrics = Column(JSON, default={}, nullable=True)
    is_automated = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime, nullable=True)
    tags = Column(JSON, default=[], nullable=True)
    integrations = Column(JSON, default={}, nullable=True)

    pipeline = relationship("Pipeline", back_populates="lanes")
    tickets = relationship("Ticket", back_populates="lane", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_pipeline_id", "pipelineId"),
        # Index("idx_status", "status"),
        # Index("idx_is_public", "is_public"),
    )
