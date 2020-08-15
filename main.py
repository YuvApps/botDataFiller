import pymongo
from userGenerator import get_bot_data

if __name__ == '__main__':

    client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
    db = client["test"]
    bot_data_col = db["bot_data"]
    users_col = db["users"]
    requests_col = db["requests"]

    mode = 1

    if mode == 1:
        all_json = get_bot_data(users_col, requests_col)

        bot_data_col.insert_many(all_json)
    else:
        bot_data_col.delete_many({})
