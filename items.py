import pymongo
from userGenerator import get_all_items

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
items_col = db["items"]

mode = 1

if mode == 1:
    json = get_all_items()
    items_col.insert_many(json)
else:
    items_col.delete_many({})
