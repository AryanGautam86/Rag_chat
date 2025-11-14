# models.py

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False)
    content = Column(Text)

DATABASE_URL = "sqlite:///./test.db"  # Can switch to Postgres later
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(expire_on_commit=True, autoflush=True, bind=engine)
Base.metadata.create_all(bind=engine)
