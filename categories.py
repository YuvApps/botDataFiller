import pymongo
from userGenerator import get_all_categories

client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
categories_col = db["categories"]

json = get_all_categories()

categories_col.insert_many(json)

# categories_col.delete_many({})
