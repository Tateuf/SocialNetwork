def get_database():
    from pymongo import MongoClient

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DB_NAME = 'SocialNetworkDB'

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)

    return connection[DB_NAME]