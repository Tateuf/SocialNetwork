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
        "likedPost" : []
    }
    dbname.User.insert_one(User)
    return dbname.User.find({"pseudo": pseudo})[0]


def findOne(pseudo):
    dbname = database.get_database()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    dbname.User.update_one({"pseudo": pseudo}, {'$set': {"lastConnection": timestamp}})
    return dbname.User.find({"pseudo": pseudo})[0]


def followOne(followerPseudo,followedPseudo):
    try :
        dbname = database.get_database()
        follower = dbname.User.find({"pseudo": followerPseudo})[0]
        followed = dbname.User.find({"pseudo": followedPseudo})[0]
        subscribes = follower["subscribe"]
        follows = followed["follower"]
        subscribes.append(followed["_id"])
        follows.append(follower["_id"])
        dbname.User.update_one({"pseudo": followerPseudo}, {'$set': {"subscribe": subscribes}})
        print(dbname.User.find({"pseudo": followerPseudo})[0])
        dbname.User.update_one({"pseudo": followedPseudo}, {'$set': {"follower": follows}})
        print(dbname.User.find({"pseudo": followedPseudo})[0])
        return followerPseudo + " follows " + followedPseudo
    except :
        return " error "


def unfollowOne(followerPseudo,followedPseudo):
    try :
        dbname = database.get_database()
        follower = dbname.User.find({"pseudo": followerPseudo})[0]
        followed = dbname.User.find({"pseudo": followedPseudo})[0]
        subscribes = follower["subscribe"]
        follows = followed["follower"]
        subscribes.remove(followed["_id"])
        follows.remove(follower["_id"])
        dbname.User.update_one({"pseudo": followerPseudo}, {'$set': {"subscribe": subscribes}})
        print(dbname.User.find({"pseudo": followerPseudo})[0])
        dbname.User.update_one({"pseudo": followedPseudo}, {'$set': {"follower": follows}})
        print(dbname.User.find({"pseudo": followedPseudo})[0])
        return followerPseudo + " unfollows " + followedPseudo
    except:
        return " error "


def verifyFollow(followerPseudo,followedPseudo):
    try :
        dbname = database.get_database()
        follower = dbname.User.find({"pseudo": followerPseudo})[0]
        followed = dbname.User.find({"pseudo": followedPseudo})[0]
        subscribes = follower["subscribe"]
        if followed["_id"] in subscribes:
            return True
        else :
            return False
    except :
        return " error "


def findIDbyPseudo(pseudo):
    dbname = database.get_database()
    return dbname.User.find({"pseudo": pseudo})[0]["_id"]

def findPseudoByID(id):
    dbname = database.get_database()
    return dbname.User.find({"pseudo": id})[0]["pseudo"]