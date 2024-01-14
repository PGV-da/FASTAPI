import psycopg2
import time
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from typing import Optional, List
from random import randrange
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="vikram", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successfull!")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error : ", error)
        time.sleep(3)
    

my_posts = [{"title" : "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite food", "content": "i like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Message": "Welcome to PGV API"}