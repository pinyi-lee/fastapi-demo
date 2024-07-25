from pydantic import BaseModel, Field

class PublishRequest(BaseModel):
    friend_id: str = Field(..., description = "friend id")