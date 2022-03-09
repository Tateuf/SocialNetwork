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

    item_1 = {
        "_id": "U1IT00001",
        "item_name": "Blender",
        "max_discount": "10%",
        "batch_number": "RR450020FRG",
        "price": 340,
        "category": "kitchen appliance"
    }

    item_2 = {
        "_id": "U1IT00002",
        "item_name": "Egg",
        "category": "food",
        "quantity": 12,
        "price": 36,
        "item_description": "brown country eggs"
    }
    collection_name.insert_many([item_1, item_2])

    print(dbname.list_collection_names())