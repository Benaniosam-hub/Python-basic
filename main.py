from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (important for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite DB
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Table
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastName = Column(String)

Base.metadata.create_all(bind=engine)

# Request model
class User(BaseModel):
    name: str
    lastName: str

@app.post("/register")
def register(user: User):
    db = SessionLocal()
    new_user = UserDB(name=user.name, lastName=user.lastName)
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": f"{user.name} {user.lastName} saved successfully"}