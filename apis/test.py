# for validate request data
import time

from fastapi import FastAPI, Header, Cookie, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import User
from schemas import UserCreate, UserOut
import logging

app = FastAPI()

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("api_duration.log")
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)



class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# apply all endpoint
@app.middleware("http")
async def timer_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} took {duration:.4f}s")
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None, p: str = None):
    return {"item_id": item_id, "q": q, "p": p}

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "is_offer": item.is_offer}

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}

@app.get("/search/")
def search(q: str = None):
    return {"query": q}

# Read Content from header
@app.get("/headers/")
def read_header(user_agent: str = Header(None)):
    return {"User-Agent": user_agent}

#Read Content from cookie
@app.get("/read_cookie/")
def read_cookie(session_id: str = Cookie(None)):
    return {"session_id": session_id}

#Dependency Injection
def common_params(q: str = None, limit: int = 10):
    return {"q": q, "limit": limit}

# 建表（第一次執行）
Base.metadata.create_all(bind=engine)

# Create
@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logging.info(user)
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read all
@app.get("/users", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Read by ID
@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update
@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = updated_user.name
    user.email = updated_user.email
    db.commit()
    db.refresh(user)
    return user

# Delete
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}