from pydantic import BaseModel, Field , field_validator
from uuid import UUID

class PublishRequest(BaseModel):
    friend_id: str = Field(..., description = "friend id")
    
    @field_validator('friend_id')
    def validate_user_id(cls, value):
        if not isinstance(value, UUID):
            raise ValueError(f"{value} is not a valid UUID")
        return value