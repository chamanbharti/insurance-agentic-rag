from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User message sent to the insurance assistant.",
    )


class ChatResponse(BaseModel):
    answer: str
    model: str
