from pydantic_settings import BaseSettings
from pydantic import Field

config_instance = None

def get_config():
    global config_instance
    if config_instance is None:
        config_instance = Settings()
    return config_instance

class Settings(BaseSettings):
    database_user: str = Field(..., json_schema_extra={"env": "DATABASE_USER"})
    database_password: str = Field(..., json_schema_extra={"env": "DATABASE_PASSWORD"})
    database_host: str = Field(..., json_schema_extra={"env": "DATABASE_HOST"})
    database_port: int = Field(..., json_schema_extra={"env": "DATABASE_PORT"})
    
    redis_host: str = Field(..., json_schema_extra={"env": "REDIS_HOST"})
    redis_port: int = Field(..., json_schema_extra={"env": "REDIS_PORT"})

    class Config:
        env_file = ".env"