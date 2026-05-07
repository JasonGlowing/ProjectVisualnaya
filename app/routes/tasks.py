from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse
from app.ai_service import categorize_task, estimate_task_time

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    category = await categorize_task(task.description)
    estimated_minutes = await estimate_task_time(task.description)

    db_task = Task(
        title=task.title,
        description=task.description,
        complexity=task.complexity,
        category=category,
        estimated_minutes=estimated_minutes,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
