from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todos" 


    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), nullable=False)  # 255는 최대 길이 예시
    completed = Column(Boolean, default=False)