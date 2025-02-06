from sqlalchemy import Table, Column, ForeignKey
from Database.base_class import Base
from sqlalchemy.dialects.postgresql import UUID

ticket_tags_association = Table(
    "ticket_tags_association",
    Base.metadata,
    Column("ticket_id", UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
