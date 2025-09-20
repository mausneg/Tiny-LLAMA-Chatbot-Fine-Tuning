from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: list[str]
