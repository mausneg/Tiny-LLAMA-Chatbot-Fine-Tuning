from pydantic import BaseModel

class Message(BaseModel):
    timestamp: str
    content: list[str]
