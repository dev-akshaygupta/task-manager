from fastapi import FastAPI, HTTPException
from schema import User as UserSchema, Login
from models import create_db_and_tables, SessionDep, User as UserModel
from contextlib import asynccontextmanager
from sqlmodel import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/home")
def home():
    return {"message": "This is home page for personal task manager application."}

@app.post("/register-user")
def register_user(user: UserSchema, session: SessionDep):
    new_user = UserModel(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get("/read-user", response_model=UserSchema)
def read_user(username: str, session: SessionDep):
    stmt = select(UserModel).where(UserModel.username == username)
    user = session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user