import json

from bson import json_util, ObjectId

import database
from datetime import datetime

def createPost(message,senderPseudo):
    dbname = database.get_database()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    Post = {
        "message": message,
        "senderPseudo" : senderPseudo,
        "creation" : timestamp,
        "likeNumber" : 0
    }
    try :
        dbname.Post.insert_one(Post)
        posts = dbname.User.find({"pseudo": senderPseudo})[0]["posts"]
        id = dbname.Post.find({"creation": timestamp})[0]["_id"]
        posts.append(str(id))
        dbname.User.update_one({"pseudo": senderPseudo}, {'$set': {"posts": posts}})
        return json.loads(json_util.dumps(dbname.Post.find({"_id" : id},{"_id" : 0})))
    except:
        return "Post failed"

def likePost(id,pseudo):
    try :
        dbname = database.get_database()
        likeNumber = dbname.Post.find({"_id": ObjectId(id)})[0]["likeNumber"]
        likeNumber += 1
        dbname.Post.update_one({"_id": ObjectId(id)}, {'$set': {"likeNumber": likeNumber}})
        likedPost = dbname.User.find({"pseudo": pseudo})[0]["likedPost"]
        likedPost.append(id)
        dbname.User.update_one({"pseudo" : pseudo}, {'$set': {"likedPost" : likedPost}})
        return " post liked "
    except :
        return " error during the like time"


def unlikePost(id,pseudo):
    try :
        dbname = database.get_database()
        likeNumber = dbname.Post.find({"_id": ObjectId(id)})[0]["likeNumber"]
        likeNumber -= 1
        dbname.Post.update_one({"_id": ObjectId(id)}, {'$set': {"likeNumber": likeNumber}})
        likedPost = dbname.User.find({"pseudo": pseudo})[0]["likedPost"]
        likedPost.remove(id)
        dbname.User.update_one({"pseudo": pseudo}, {'$set': {"likedPost": likedPost}})
        return " post unliked "
    except :
        return " error during the like time"


def verifyLike(id,pseudo):
    try :
        dbname = database.get_database()
        if id in dbname.User.find({"pseudo": pseudo})[0]["likedPost"]:
            return True
        else :
            return False
    except :
        return "error"

def getAllMyPost(pseudo):
    try :
        dbname = database.get_database()
        subscribes = dbname.User.find({"pseudo": pseudo})[0]["subscribe"]
        posts = dbname.Post.find({"senderPseudo" : { "$in" : subscribes }}).sort("creation")
        return json.loads(json_util.dumps(posts))[::-1]
    except :
        return "error"