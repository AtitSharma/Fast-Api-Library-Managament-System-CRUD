from fastapi import FastAPI
from app import models
from app.database import engine
# from sqlalchemy.orm import Session
from app.routers import book,library,users

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(book.router)
# app.include_router(library.router)
app.include_router(users.router)



