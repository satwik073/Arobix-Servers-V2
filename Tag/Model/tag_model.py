import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    JSON,
    Integer,
    Text,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Database.base_class import Base
from Configs.configuration import AccountStatus


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


    subAccountId = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    subAccount = relationship("SubAccount", back_populates="tags")

    tickets = relationship("Ticket", back_populates="tag", cascade="all, delete-orphan")
    miscdata = Column(JSON, default={}, nullable=True)
    
    priority = Column(Integer, default=1, nullable=True)  # Can be used for sorting or importance
    is_active = Column(Boolean, default=True, nullable=False)  # Soft delete mechanism
    category = Column(String, nullable=True)  # Used for categorizing the tag
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Assign a user to the tag
    

    __table_args__ = (
        # Index("idx_sub_account_id", "subAccountId"),
        Index("idx_category", "category"),
    )
