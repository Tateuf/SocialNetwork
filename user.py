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
        "lastConnection": timestamp
    }
    dbname.User.insert_one(User)
    return dbname.User.find({"pseudo": pseudo})[0]


def findOne(pseudo):
    dbname = database.get_database()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    dbname.User.update_one({"pseudo": pseudo}, {'$set': {"lastConnection": timestamp}})
    return dbname.User.find({"pseudo": pseudo})[0]
