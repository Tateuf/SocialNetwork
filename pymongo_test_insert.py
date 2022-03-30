from datetime import datetime
import authentication
import user


def get_database():
    from pymongo import MongoClient

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DB_NAME = 'SocialNetworkDB'

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)

    return connection[DB_NAME]


if __name__ == "__main__":
    dbname = get_database()
    collection_name = dbname["User"]
    collection_post = dbname["Post"]
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    User_test = {
        "pseudo": "Blender",
        "posts": [],
        "subscribe": [],
        "follower": [],
        "notification": [],
        "lastConnection": timestamp
    }

    Post_test = {
        "tags" : [],
        "message" : "Hello bg",
        "photo" : [],
        "senderID" : "id45",
        "likeNumber" : 0
    }

    #print(authentication.signUp("Tateuf","123"))
    #collection_name.insert_one(User_test)
    #collection_post.insert_one(Post_test)
    #crypto.addUser("test","password")
    #authentication.verificationUser("test","password")
    #authentication.verificationUser("test2","password")
    #authentication.verificationUser("test","password2")
    print(user.verifyFollow("Tateuf","Troy"))
    #print(authentication.signIn("Tateuf","123"))
    #print(dbname.list_collection_names())