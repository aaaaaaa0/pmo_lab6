from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    pclass = Column(Integer)
    sex = Column(String)
    age = Column(Float)
    sibsp = Column(Integer)
    parch = Column(Integer)
    fare = Column(Float)
    embarked = Column(String)
    name = Column(String)
    survived_pred = Column(Integer)
    probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()