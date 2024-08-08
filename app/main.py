from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, database, models, schemas

app = FastAPI()

def get_db():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.read_tasks(db=db)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.read_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int,task: schemas.TaskCreate, db: Session = Depends(get_db)):
    update_task = crud.update_task(task_id=task_id,task=task,db=db)
    if update_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    delete_task = crud.delete_task(db=db, task_id=task_id)
    if delete_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}