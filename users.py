import pymongo
import random
from userGenerator import get_user


client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
users_col = db["users"]
users_set = set()
users_arr = []

mode = 1

if mode == 1:
    for index in range(1, 1000):
        users_arr.append(get_user(index))

    users_col.insert_many(users_arr)
else:
    users_col.delete_many({})
