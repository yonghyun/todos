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
    except Exception as e:
        print(f"실행 오류: {e}")
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # DB에서 모든 To-Do 항목을 내림차순으로 가져오기
    todos = db.query(Todo).order_by(Todo.id.desc()).all()  # 가장 최근 항목이 위로 오도록 내림차순 정렬
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos,
    })

@app.post("/add")
async def add_task(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    # 새로운 To-Do 항목을 추가하는 라우트
    new_todo = Todo(task=task)  # 입력된 task 값을 사용해 새 Todo 객체 생성
    db.add(new_todo)  # DB에 새 To-Do 항목 추가
    db.commit()  # DB에 변경사항 커밋
    db.refresh(new_todo)  # DB에서 새 항목을 다시 로드하여 객체 갱신
    return RedirectResponse(url="/", status_code=303)  # 홈 페이지로 리디렉션

@app.get("/edit/{id}")
async def edit_task(request: Request, id: int, db: Session = Depends(get_db)):
    # 특정 To-Do 항목을 편집하는 페이지
    todo = db.query(Todo).filter(Todo.id == id).first()  # 해당 ID의 To-Do 항목 검색
    if todo is None:
        return RedirectResponse(url="/", status_code=404)  # 항목이 없으면 404로 리디렉션
    todos = db.query(Todo).all()  # 모든 To-Do 항목 가져오기
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo, "todos": todos})

@app.post("/edit/{id}")
async def update_task(id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    # To-Do 항목을 업데이트하는 라우트
    todo = db.query(Todo).filter(Todo.id == id).first()  # 해당 ID의 To-Do 항목 검색
    if todo:
        todo.task = task  # task 내용 업데이트
        todo.completed = completed  # completed 상태 업데이트
        db.commit()  # DB에 변경사항 커밋
    return RedirectResponse(url="/", status_code=303)  # 홈 페이지로 리디렉션

@app.get("/delete/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    # 특정 To-Do 항목을 삭제하는 라우트
    todo = db.query(Todo).filter(Todo.id == id).first()  # 해당 ID의 To-Do 항목 검색
    if todo:
        db.delete(todo)  # 항목 삭제
        db.commit()  # DB에 변경사항 커밋
    return RedirectResponse(url="/", status_code=303)  # 홈 페이지로 리디렉션

if __name__ == "__main__":
    # 앱 실행 설정: 개발 환경에서 로컬 서버 실행
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
