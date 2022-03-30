import hashlib
import os

from bson import json_util

import database
import user
import json

def signUp(pseudo, code):
    dbname = database.get_database()
    try:
        dbname.User.find({"pseudo": pseudo})[0]
        return pseudo + " already use"
    except:
        try:
            currentUser = user.addUser(pseudo)
            salt = os.urandom(32)  # A new salt for this user
            key = hashlib.pbkdf2_hmac('sha256', code.encode('utf-8'), salt, 100000)
            collection_auth = dbname["Authentication"]
            Authentication = {
                    "pseudo": pseudo,
                    "key": key,
                    "salt": salt
            }
            collection_auth.insert_one(Authentication)
            return pseudo + " has been created"
        except:
            return "DB failed"


def signIn(pseudo, code):
    dbname = database.get_database()
    try:
        information = dbname.Authentication.find({"pseudo": pseudo})
        key = information[0]['key']
        salt = information[0]['salt']
        keyVerification = hashlib.pbkdf2_hmac('sha256', code.encode('utf-8'), salt, 100000)
        if key == keyVerification:
            try :
                currentUser = user.findOne(pseudo)
                return json.loads(json_util.dumps(currentUser))
            except :
                return "User not in the db"

        else:
            print("Erreur dans le mot de passe")
            return False
    except:
        print("Erreur dans le pseudo")
        return False
