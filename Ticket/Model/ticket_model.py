import uuid
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum, JSON, Boolean,Index, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from Delta.ticket_tags_association import ticket_tags_association
from Database.base_class import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    laneId = Column(UUID(as_uuid=True), ForeignKey("lanes.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, default=0, nullable=False)
    value = Column(Float, nullable=True)
    customerId = Column(UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    assignedUserId = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum("Open", "In Progress", "Closed", "Resolved", name="ticket_status_enum"), default="Open", nullable=False)
    priority = Column(Enum("Low", "Medium", "High", name="ticket_priority_enum"), default="Medium", nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    tags = Column(JSON, default=[])
    custom_fields = Column(JSON, default={})
    is_public = Column(Boolean, default=False, nullable=False)
    assigned_user = relationship("User", back_populates="assigned_tickets")
    # Relationships
    lane = relationship("Lane", back_populates="tickets")
    customer = relationship("Contact", back_populates="tickets")
    user = relationship("User", back_populates="assigned_tickets")
    tags = relationship("Tag", secondary=ticket_tags_association, back_populates="tickets")
    contact = relationship("Contact", back_populates="tickets")

    __table_args__ = (
        Index("idx_ticket_lane_id", "laneId"),
        Index("idx_ticket_customer_id", "customerId"),
        Index("idx_ticket_assigned_user_id", "assignedUserId"),
        Index("idx_ticket_priority", "priority"),
        Index("idx_ticket_status", "status"),
    )
