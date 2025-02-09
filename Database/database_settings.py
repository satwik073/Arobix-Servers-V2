# import logging as __LOGS_SESSION__
# from sqlalchemy.orm import sessionmaker as __SESSION_MAKER__
# from sqlalchemy.exc import SQLAlchemyError as __SQLALCHEMY_ERROR__
# from Core.config_parameters import settings as __CONFIG_RULES__
# from sqlalchemy.ext.asyncio import create_async_engine as __RUNABLE_ENGINES__, AsyncSession as __ASYNC_SESSIONS__

# # ✅ Setup Logging for SQLAlchemy
# asyncLoggers = __LOGS_SESSION__.getLogger('sqlalchemy.engine')
# asyncLoggers.setLevel(__LOGS_SESSION__.INFO if __CONFIG_RULES__.DEBUG else __LOGS_SESSION__.WARNING)

# # ✅ Define the Async Engine for FastAPI
# engine = __RUNABLE_ENGINES__(
#     __CONFIG_RULES__.DATABASE_URL,
#     echo=__CONFIG_RULES__.DEBUG,
#     pool_size=__CONFIG_RULES__.MAX_POOL_SIZE,
#     max_overflow=__CONFIG_RULES__.MAX_OVERFLOW,
#     pool_timeout=__CONFIG_RULES__.POOL_TIMEOUT,
#     pool_recycle=__CONFIG_RULES__.POOL_RECYCLE,
#     future=True,
# )

# # ✅ Async Session Factory
# async_session = __SESSION_MAKER__(
#     bind=engine,
#     class_=__ASYNC_SESSIONS__,
#     expire_on_commit=False
# )

# # ✅ Dependency to Get DB Session in FastAPI
# async def get_database_secure_connection():
#     async with async_session() as session:
#         try:
#             yield session
#         except __SQLALCHEMY_ERROR__ as e:
#             asyncLoggers.error(f"Database error occurred: {str(e)}")
#             raise
#         finally:
#             await session.close()

from motor.motor_asyncio import AsyncIOMotorClient
from Core.config_parameters import settings
import logging
from pymongo.errors import ConfigurationError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None


async def connect_to_mongo():
    MongoDB.client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    MongoDB.db = MongoDB.client["arobix-prod-server"]
    print("✅ MongoDB connected")

# Disconnect from MongoDB on app shutdown
async def close_mongo_connection():
    if MongoDB.client:
        MongoDB.client.close()
        print("🛑 MongoDB connection closed")
        
try:
    # Create client immediately
    client = AsyncIOMotorClient(settings.DATABASE_URL)

    # Explicitly set database name
    database = client['arobix-prod-server']  # Using 'arobix' as the database name

    # Initialize collections immediately
    users_collection = database.users
    organizations_collection = database.organizations

    logger.info("🚀 MongoDB collections initialized")

except Exception as e:
    logger.error(f"Failed to initialize MongoDB: {str(e)}")
    raise

# Simple connection verification function
async def verify_connection():
    try:
        # Test connection
        await client.admin.command('ping')
        # Test collections
        await users_collection.find_one({})
        await organizations_collection.find_one({})
        logger.info("✅ MongoDB connection verified successfully")
        return True
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        return False

# Simple getter for FastAPI dependency
async def get_db():
    await verify_connection()
    return database

# Startup event
async def startup_event():
    await verify_connection()