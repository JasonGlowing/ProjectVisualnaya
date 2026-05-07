from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    complexity: str = "medium"


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    estimated_minutes: int
    complexity: str
    completed: bool

    class Config:
        from_attributes = True
