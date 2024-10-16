from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_env import user, password, host, db_name

# MySQL 데이터베이스 URL 생성
db_url = f"mysql+pymysql://{user}:{password}@{host}:3306/{db_name}"
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
