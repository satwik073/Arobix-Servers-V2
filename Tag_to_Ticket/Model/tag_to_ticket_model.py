from sqlalchemy import (
    Column, String, Index, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from Database.base_class import Base

class TagToTicket(Base):
    __tablename__ = "tag_to_ticket"

    # Ensure the 'id' field is properly declared with mapped_column and Mapped[]
    id: Mapped[str] = mapped_column(String, primary_key=True, default=None, nullable=False)
    A: Mapped[str] = mapped_column(String, nullable=False)
    B: Mapped[str] = mapped_column(String, nullable=False)

    __table_args__ = (
        Index("idx_tag_to_ticket_B", "B"),
        UniqueConstraint("A", "B", name="_TagToTicket_AB_unique"),
    )
