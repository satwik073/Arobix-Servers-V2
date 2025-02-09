# from pydantic_settings import BaseSettings
# from pydantic import Field
# from typing import Optional
# import os as __OPERATING__SYSTEM__
# from Configs.configuration import Criticals
# class Settings(BaseSettings):
#     ENV: str = Field(default="staging", env="ENV")
#     DATABASE_URL: str = Field(..., env="DATABASE_URL")
#     SECRET_KEY: str = Field(..., env="SECRET_KEY")
#     DEBUG: bool = Field(default=False, env="DEBUG")
#     MAX_POOL_SIZE: int = Field(default=10, env="MAX_POOL_SIZE")
#     MAX_OVERFLOW: int = Field(default=20, env="MAX_OVERFLOW")
#     POOL_TIMEOUT: int = Field(default=30, env="POOL_TIMEOUT")
#     POOL_RECYCLE: int = Field(default=1800, env="POOL_RECYCLE")
#     LOG_LEVEL : str = Criticals['__INFO__']['value']
#     class Config:
#         env_file = f"__ENVS__/.env.{__OPERATING__SYSTEM__.getenv('ENV', 'staging')}"
#         env_file_encoding = 'utf-8'


# settings = Settings()


from pydantic_settings import BaseSettings
from pydantic import Field
import os as __OPERATING__SYSTEM__

class Settings(BaseSettings):
    ENV: str = Field(default="staging", env="ENV")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # ✅ MongoDB URL
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    DEBUG: bool = Field(default=False, env="DEBUG")
    MAX_POOL_SIZE: int = Field(default=10, env="MAX_POOL_SIZE")
    MAX_OVERFLOW: int = Field(default=20, env="MAX_OVERFLOW")
    POOL_TIMEOUT: int = Field(default=30, env="POOL_TIMEOUT")
    POOL_RECYCLE: int = Field(default=1800, env="POOL_RECYCLE")
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = f"__ENVS__/.env.{__OPERATING__SYSTEM__.getenv('ENV', 'staging')}"
        env_file_encoding = 'utf-8'

settings = Settings()
