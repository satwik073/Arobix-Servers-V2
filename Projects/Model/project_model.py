import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    Text,
    JSON,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Database.base_class import Base
from Configs.configuration import ProjectStatus


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False)
    start_date = Column(DateTime, default=func.now(), nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget = Column(JSON, default={}, nullable=True)  # Budget-related information
    miscdata = Column(JSON, default={}, nullable=True)  # Customizable fields

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    
    # ✅ Relationship with Organization
    organization = relationship("Organization", back_populates="projects")

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_project_name", "name"),
        Index("idx_organization_id", "organization_id"),
        Index("idx_status_value", "status"),
    )
