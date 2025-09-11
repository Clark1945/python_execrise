import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Config the database connection
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/testdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
Base = declarative_base()

# Dependency Injection：provide Session when needs
def get_db():
    start = time.time()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        duration=time.time() - start
        print(f"[LOG] API took {duration:.4f} seconds")