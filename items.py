import pymongo
from userGenerator import get_all_items


def items_creation(mode):
    if mode > 0:
        client = pymongo.MongoClient(
            "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
        db = client["test"]
        items_col = db["items"]

        if mode == 1:
            json = get_all_items()
            items_col.insert_many(json)
        else:
            items_col.delete_many({})
