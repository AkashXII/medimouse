from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_URL = "sqlite:///./medimouse.db"

engine = create_engine(SQL_URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
