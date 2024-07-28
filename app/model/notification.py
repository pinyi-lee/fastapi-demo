from pydantic import BaseModel, Field , field_validator
from uuid import UUID

class PublishRequest(BaseModel):
    friend_id: str = Field(..., description = "friend id")
    
    @field_validator('friend_id')
    def validate_user_id(cls, value):
        try:
            uuid_obj = UUID(value, version=4)
            if str(uuid_obj) == value:
                return value
            raise ValueError(f"{value} is not a valid UUID")
        except ValueError:
            raise ValueError(f"{value} is not a valid UUID")