import logging as __LOGS_SESSION__
from sqlalchemy.orm import sessionmaker as __SESSION_MAKER__
from sqlalchemy.exc import SQLAlchemyError as __SQLALCHEMY_ERROR__
from Core.config_parameters import settings as __CONFIG_RULES__
from sqlalchemy.ext.asyncio import create_async_engine as __RUNABLE_ENGINES__ , AsyncSession as __ASYNC_SESSIONS__

asyncLoggers = __LOGS_SESSION__.getLogger('sqlalchemy.engine')
asyncLoggers.setLevel(__LOGS_SESSION__.INFO if __CONFIG_RULES__.DEBUG else __LOGS_SESSION__.WARNING)

engine = __RUNABLE_ENGINES__(
    __CONFIG_RULES__.DATABASE_URL,
    echo = __CONFIG_RULES__.DEBUG,
    pool_size=__CONFIG_RULES__.MAX_POOL_SIZE,
    max_overflow=__CONFIG_RULES__.MAX_OVERFLOW,
    pool_timeout=30,  
    future=True,
)


async_session = __SESSION_MAKER__(
    bind=engine,
    class_= __ASYNC_SESSIONS__,
    expire_on_commit=False
)

async def get_database_secure_connection():
    async with async_session() as session:
        try:
            yield session
        except __SQLALCHEMY_ERROR__ as e:
            asyncLoggers.error(f"Database error occurred: {str(e)}")
            raise
        finally:
            await session.close()