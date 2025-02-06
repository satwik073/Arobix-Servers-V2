import asyncio
import logging
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from Database.base_class import Base
from Core.config_parameters import settings

# ✅ Setup Logging
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# ✅ Define Database URL from Settings
DATABASE_URL = settings.DATABASE_URL

# ✅ Create Async Engine for Alembic
engine = create_async_engine(
    DATABASE_URL,
    poolclass=pool.NullPool,  # ✅ Important for Alembic Migrations
    future=True,
)

# ✅ Function to run migrations asynchronously
async def run_migrations_online():
    """Runs Alembic migrations in an asynchronous context."""
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: context.configure(
            connection=sync_conn,  # ✅ Fix: Pass connection correctly
            target_metadata=Base.metadata,
            compare_type=True
        ))

        await conn.run_sync(lambda sync_conn: context.run_migrations())  # ✅ Fix: Ensure correct function call

# ✅ Run Migrations in Async Mode
asyncio.run(run_migrations_online())
