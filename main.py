from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
import uvicorn
from database import SessionLocal, engine
from models import Todo

# 모델 초기화
Todo.metadata.create_all(bind=engine)

app = FastAPI()

# 템플릿 및 정적 파일 경로 설정
abs_path = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=f"{abs_path}/templates")
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")

# 데이터베이스 세션 종속성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    hello = "Appreciate this picture"
    todos = db.query(Todo).all()  # DB에서 모든 To-Do 항목 가져오기
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos,
        "hello": hello
    })

@app.post("/add")
async def add_task(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    new_todo = Todo(task=task)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{id}")
async def edit_task(request: Request, id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo is None:
        return RedirectResponse(url="/", status_code=404)
    todos = db.query(Todo).all()
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo, "todos": todos})

@app.post("/edit/{id}")
async def update_task(id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        todo.task = task
        todo.completed = completed  # `completed` 필드 업데이트
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
