from fastapi import FastAPI

from app.database import Base, engine
from app.routes.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Task Planner",
    description="Умный планировщик задач с AI-категоризацией и оценкой времени.",
    version="1.0.0",
)

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Smart Task Planner API is running"}
