from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title = task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def read_tasks(db:Session):
    return db.query(models.Task).all()

def read_task(db:Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db:Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db:Session, task_id:int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None

    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}