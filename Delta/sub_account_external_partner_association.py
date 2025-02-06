from sqlalchemy import Table, MetaData
from sqlalchemy import ( Column, UUID, ForeignKey)
from Database.base_class import Base
metadata = MetaData()
sub_account_external_partner_association = Table(
    "sub_account_external_partner_association",
    Base.metadata,
    Column("sub_account_id", UUID(as_uuid=True), ForeignKey("sub_account.id", ondelete="CASCADE"), primary_key=True),
    Column("external_partner_id", UUID(as_uuid=True), ForeignKey("external_partner.id", ondelete="CASCADE"), primary_key=True),  # Corrected reference
)
