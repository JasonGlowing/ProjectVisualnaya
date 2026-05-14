from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

app = FastAPI(
    title="Simple Smart Task Planner",
    description="Простой умный планировщик задач на FastAPI",
    version="1.0.0"
)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, default="другое")
    estimated_minutes = Column(Integer, default=30)
    complexity = Column(String, default="medium")
    completed = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


class TaskCreate(BaseModel):
    title: str
    description: str
    complexity: str = "medium"


from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    estimated_minutes: int
    complexity: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def guess_category(description: str) -> str:
    text = description.lower()

    if any(word in text for word in ["работа", "проект", "отчет", "клиент", "созвон"]):
        return "работа"

    if any(word in text for word in ["спорт", "тренировка", "сон", "здоровье", "врач"]):
        return "здоровье"

    if any(word in text for word in ["учить", "курс", "урок", "книга", "экзамен", "python", "fastapi"]):
        return "обучение"

    if any(word in text for word in ["дом", "семья", "магазин", "уборка", "личное"]):
        return "личное"

    return "другое"


def estimate_minutes(description: str, complexity: str) -> int:
    minutes = 30

    if len(description) > 80:
        minutes += 30

    if complexity == "high":
        minutes += 60
    elif complexity == "low":
        minutes -= 10

    return max(minutes, 10)


@app.get("/")
def root():
    return {"message": "Simple Smart Task Planner работает"}


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        category=guess_category(task.description),
        estimated_minutes=estimate_minutes(task.description, task.complexity),
        complexity=task.complexity,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )