from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from Database.base_class import Base

sub_account_user_association = Table(
    "sub_account_user_association",
    Base.metadata,
    Column("sub_account_id", UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)
