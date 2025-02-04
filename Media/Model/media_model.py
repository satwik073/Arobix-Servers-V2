from sqlalchemy import (
    Column, String, DateTime, UUID, ForeignKey, JSON, Boolean,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from Database.base_class import Base
class Media(Base):
    __tablename__ = "media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    type = Column(String, nullable=True)
    name = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    miscdata = Column(JSON, default={})  # Stores extra information about media

    # Relationships
    sub_account = relationship("SubAccount", back_populates="media")

    __table_args__ = (
        Index("idx_media_sub_account_id", "sub_account_id"),
    )
