from typing import Annotated
from fastapi import FastAPI, Depends, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Database connection
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Create DB and all the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# User Model
class User(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    name : str 
    username : str = Field(index=True)
    password : str