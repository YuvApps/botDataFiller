import pymongo
import random
from userGenerator import get_req_by_user


def requests_creation(mode):
    if mode > 0:
        client = pymongo.MongoClient(
                "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
        db = client["test"]
        requests_col = db["requests"]
        requests_arr = []

        if mode == 1:
            for index in range(30000):
                requests_arr.append(get_req_by_user(random.randint(1, 1000)))

            requests_col.insert_many(requests_arr)
        else:
            requests_col.delete_many({})
