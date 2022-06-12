import json
import string
from array import array
from typing import Optional

import bson
from fastapi import FastAPI
from pydantic import BaseModel
import authentication
import post
import user

app = FastAPI()


class Credentials(BaseModel):
    pseudo: str
    code: str

class Poster(BaseModel):
    message : str
    senderPseudo : str

class Search(BaseModel):
    research : str

class Follow(BaseModel):
    followed : str
    follower : str

class LikePost(BaseModel):
    id : str
    pseudo : str

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
    return post.createPost(poster.message, poster.senderPseudo)

@app.post("/users")
def read_root(search : Search):
    return user.findAll(search.research)

@app.post("/user")
def read_root(pseudo : Search):
    return user.findOne(pseudo.research)

@app.get("/")
def read_root():
    return "Hello World"

@app.put('/follow')
def read_root(follow : Follow):
    return user.followOne(follow.follower, follow.followed)

@app.put('/unfollow')
def read_root(follow : Follow):
    return user.unfollowOne(follow.follower, follow.followed)

@app.get('/verify_follow')
def read_root(follow : Follow):
    return user.verifyFollow(follow.follower, follow.followed)

@app.put('/like')
def read_root(likePost : LikePost):
    return post.likePost(likePost.id, likePost.pseudo)

@app.put('/unlike')
def read_root(likePost : LikePost):
    return post.unlikePost(likePost.id, likePost.pseudo)

@app.get('/verify_like')
def read_root(likePost : LikePost):
    return post.verifyLike(likePost.id, likePost.pseudo)

@app.post('/postByUser')
def read_root(search : Search):
    return user.getPostfromUser(search.research)

@app.get('/subscribe_post')
def read_root(search : Search):
    return post.getAllMyPost(search.research)

