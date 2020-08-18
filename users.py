import pymongo
from userGenerator import get_user


def users_creation(mode):
    if mode > 0:
        client = pymongo.MongoClient(
                "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
        db = client["test"]
        users_col = db["users"]
        users_arr = []

        if mode == 1:
            for index in range(1, 1000):
                users_arr.append(get_user(index))

            users_col.insert_many(users_arr)
        else:
            users_col.delete_many({})
