from sqlalchemy import Table, Column, ForeignKey
from Database.base_class import Base
from sqlalchemy.dialects.postgresql import UUID

pipeline_tags = Table(
    "pipeline_tags",
    Base.metadata,
    Column("pipeline_id", UUID(as_uuid=True), ForeignKey("pipelines.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
