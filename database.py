from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# MySQL 연결 정보 가져오기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# MySQL 데이터베이스 URL 생성
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 데이터베이스에 연결하는 엔진을 생성하는 함수
engine = create_engine(DATABASE_URL)

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
Base = declarative_base()
