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
        "likeNumber" : 0,
        "likers" : []
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

def likePost(author, pseudo, creation):
    try :
        dbname = database.get_database()
        print(author, pseudo, creation)
        post = dbname.Post.find({"senderPseudo": author, "creation" : creation})[0]
        likeNumber = post["likeNumber"]
        try :
            likers = post["likers"]
        except :
            likers = []
        likers.append(pseudo)
        postID = post["_id"]
        likeNumber += 1
        dbname.Post.update_one({"senderPseudo": author, "creation" : creation}, {'$set': {"likeNumber": likeNumber, "likers": likers}})
        likedPost = dbname.User.find({"pseudo": pseudo})[0]["likedPost"]
        likedPost.append(str(postID))
        dbname.User.update_one({"pseudo" : pseudo}, {'$set': {"likedPost" : likedPost}})
        response = {
            "result": True
        }
        return response
    except :
        response = {
            "result": "error"
        }
        return response


def unlikePost(author, pseudo, creation):
    try :
        dbname = database.get_database()
        post = dbname.Post.find({"senderPseudo": author, "creation": creation})[0]
        likeNumber = post["likeNumber"]
        postID = post["_id"]
        likeNumber -= 1
        try :
            likers = post["likers"]
            likers.remove(pseudo)
        except :
            likers = []
        dbname.Post.update_one({"senderPseudo": author, "creation": creation}, {'$set': {"likeNumber": likeNumber, "likers": likers}})
        likedPost = dbname.User.find({"pseudo": pseudo})[0]["likedPost"]
        likedPost.remove(str(postID))
        dbname.User.update_one({"pseudo": pseudo}, {'$set': {"likedPost": likedPost}})
        response = {
            "result": True
        }
        return response
    except :
        response = {
            "result": False
        }
        return response


def verifyLike(author, pseudo, creation):
    response = {
        "result": False
    }
    try :
        dbname = database.get_database()
        id = dbname.Post.find({"senderPseudo": author, "creation": creation})[0]["_id"]
        if str(id) in dbname.User.find({"pseudo": pseudo})[0]["likedPost"]:
            response["result"] = True
            return response
        else :
            return response
    except :
        return response

def getAllMyPost(pseudo):
    try :
        dbname = database.get_database()
        subscribes = dbname.User.find({"pseudo": pseudo})[0]["subscribe"]
        posts = dbname.Post.find({"senderPseudo" : { "$in" : subscribes }}).sort("creation")
        response = {
            "posts" : json.loads(json_util.dumps(posts))[::-1]
        }
        return response
    except :
        return "error"