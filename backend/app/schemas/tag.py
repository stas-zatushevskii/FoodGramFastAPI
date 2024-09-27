from pydantic import BaseModel, Field

class Tag(BaseModel):
    id: int
    name: str
    color: str
    slug: str