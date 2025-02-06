import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Boolean,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Database.base_class import Base

class ExternalPartner(Base):
    __tablename__ = "external_partner"  # Ensure consistency

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    contact_email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    website = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    miscdata = Column(JSON, default={})  # Allows flexible extensions for future features

    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship with SubAccount through the association table
    subAccounts = relationship(
        "SubAccount",
        back_populates="externalPartners",
        secondary="sub_account_external_partner_association"
    )

    # Indexes for performance optimization
    __table_args__ = (
        Index("idx_external_partner_name", "name"),
        Index("idx_external_partner_email", "contact_email"),
        Index("idx_external_partner_company", "company_name"),
    )
