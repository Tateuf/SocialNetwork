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
        "creation" : timestamp
    }
    try :
        dbname.Post.insert_one(Post)
        return Post
    except :
        return "Post failed"