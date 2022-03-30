import json
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import authentication
import post

app = FastAPI()


class Credentials(BaseModel):
    pseudo: str
    code: str

class Poster(BaseModel):
    post : dict

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/signUp")
def read_root(credentials: Credentials):
    test = authentication.signUp(credentials.pseudo, credentials.code)
    return json.dumps(test)


@app.post("/signIn")
def read_root(credentials: Credentials):
    return authentication.signIn(credentials.pseudo, credentials.code)

@app.post("/post")
def read_root(poster: Poster):
    return post.createPost(poster.post)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
