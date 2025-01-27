from fastapi import FastAPI
from Core.config_parameters import settings
from Database.database_settings import engine
from Database.base_class import Base
from Routes.routing_support import router as user_router  # Import the user router

app = FastAPI()

# Include the user router
app.include_router(user_router, prefix="/api/v1", tags=["Users"])

@app.get("/")
async def default():
    return {"message": "Welcome to the FastAPI application"}

@app.on_event("startup")
async def startup():
    print(f"Starting application in {settings.ENV} environment...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
