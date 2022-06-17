import json

from bson import json_util, ObjectId

import pymongo_test_insert
import authentication
import database
from datetime import datetime


def addUser(pseudo):
    dbname = database.get_database()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    User = {
        "pseudo": pseudo,
        "posts": [],
        "subscribe": [],
        "follower": [],
        "notification": [],
        "lastConnection": timestamp,
        "likedPost": []
    }
    dbname.User.insert_one(User)
    return dbname.User.find({"pseudo": pseudo})[0]

def find(pseudo):
    dbname = database.get_database()
    return json.loads(json_util.dumps(dbname.User.find({"pseudo": pseudo}, {"_id" : 0})[0]))

def findAll(research):
    dbname = database.get_database()
    data = dbname.User.find({"pseudo": {'$regex': '^' + research, '$options': 'i'}},{"_id":0})
    response = {
        "users" : json.loads(json_util.dumps(data))
    }
    return response



def findOne(pseudo):
    dbname = database.get_database()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    dbname.User.update_one({"pseudo": pseudo}, {'$set': {"lastConnection": timestamp}})
    data = dbname.User.find({"pseudo": pseudo})
    return json.loads(json_util.dumps(data))


def followOne(followerPseudo, followedPseudo):
    try:
        dbname = database.get_database()
        follower = dbname.User.find({"pseudo": followerPseudo})[0]
        followed = dbname.User.find({"pseudo": followedPseudo})[0]
        subscribes = follower["subscribe"]
        follows = followed["follower"]
        subscribes.append(followed["pseudo"])
        follows.append(follower["pseudo"])
        dbname.User.update_one({"pseudo": followerPseudo}, {'$set': {"subscribe": subscribes}})
        print(dbname.User.find({"pseudo": followerPseudo})[0])
        dbname.User.update_one({"pseudo": followedPseudo}, {'$set': {"follower": follows}})
        print(dbname.User.find({"pseudo": followedPseudo})[0])
        response = {
            "result": True
        }
        return response
    except:
        response = {
            "result": False
        }
        return response


def unfollowOne(followerPseudo, followedPseudo):
    response = {
        "result": True
    }
    try:
        dbname = database.get_database()
        follower = dbname.User.find({"pseudo": followerPseudo})[0]
        followed = dbname.User.find({"pseudo": followedPseudo})[0]
        subscribes = follower["subscribe"]
        follows = followed["follower"]
        subscribes.remove(followed["pseudo"])
        follows.remove(follower["pseudo"])
        dbname.User.update_one({"pseudo": followerPseudo}, {'$set': {"subscribe": subscribes}})
        print(dbname.User.find({"pseudo": followerPseudo})[0])
        dbname.User.update_one({"pseudo": followedPseudo}, {'$set': {"follower": follows}})
        print(dbname.User.find({"pseudo": followedPseudo})[0])
        return response
    except:
        response = {
            "result": False
        }
        return response


def verifyFollow(followerPseudo, followedPseudo):
    response = {
        "result": False
    }
    try:
        dbname = database.get_database()
        follower = dbname.User.find({"pseudo": followerPseudo})[0]
        followed = dbname.User.find({"pseudo": followedPseudo})[0]
        subscribes = follower["subscribe"]
        if followed["pseudo"] in subscribes:
            response["result"] = True
            return response
        else:
            return response
    except:
        return response


def findIDbyPseudo(pseudo):
    dbname = database.get_database()
    return dbname.User.find({"pseudo": pseudo})[0]["_id"]


def findPseudoByID(id):
    dbname = database.get_database()
    return dbname.User.find({"pseudo": id})[0]["pseudo"]


def getPostfromUser(pseudo):
    try:
        dbname = database.get_database()
        postsID = dbname.User.find({"pseudo": pseudo})[0]["posts"]
        postObjectId = []
        for elem in postsID:
            postObjectId.append(ObjectId(elem))
        posts = dbname.Post.find({"_id": {"$in": postObjectId}}).sort("creation")
        response = {
            "posts" : json.loads(json_util.dumps(posts))[::-1]
        }
        return response
    except:
        return "error"
