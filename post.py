import database
from datetime import datetime

def createPost(jsonObject):
    dbname = database.get_database()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    Post = {
        "tags" : jsonObject["tags"],
        "message": jsonObject["message"],
        "photo": jsonObject["photo"],
        "senderId" : jsonObject["senderId"],
        "creation" : timestamp,
        "likeNumber" : 0
    }
    try :
        dbname.Post.insert_one(Post)
        return Post
    except :
        return "Post failed"

def likePost(id,pseudo):
    try :
        dbname = database.get_database()
        likeNumber = dbname.Post.find({"_id": id})[0]["likeNumber"]
        likeNumber += 1
        dbname.Post.update_one({"_id": id}, {'$set': {"likeNumber": likeNumber}})
        likedPost = dbname.User.find({"pseudo": pseudo})[0]["likedPost"]
        likedPost.append(id)
        dbname.User.update_one({"pseudo" : pseudo}, {'$set': {"likedPost" : likedPost}})
        return " post liked "
    except :
        return " error during the like time"


def unlikePost(id,pseudo):
    try :
        dbname = database.get_database()
        likeNumber = dbname.Post.find({"_id": id})[0]["likeNumber"]
        likeNumber -= 1
        dbname.Post.update_one({"_id": id}, {'$set': {"likeNumber": likeNumber}})
        likedPost = dbname.User.find({"pseudo": pseudo})[0]["likedPost"]
        likedPost.pop(id)
        dbname.User.update_one({"pseudo": pseudo}, {'$set': {"likedPost": likedPost}})
        return " post liked "
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