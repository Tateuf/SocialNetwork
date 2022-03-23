import json
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import authentication

app = FastAPI()


class Credentials(BaseModel):
    pseudo: str
    code: str


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
