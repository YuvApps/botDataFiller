import pymongo
from questions import questions_creation
from categories import categories_creation
from users import users_creation
from requests import requests_creation
from bot_data import bot_data_creation

if __name__ == '__main__':
    client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/walletDB?retryWrites=true&w=majority")
    db = client["walletDB"]

    questions_mode = 1
    categories_mode = 1
    users_mode = 1
    requests_mode = 1
    bot_data_mode = 1

    questions_creation(db, questions_mode)
    print("questions_creation finished in mode " + str(questions_mode))
    categories_creation(db, categories_mode)
    print("categories_creation finished in mode " + str(categories_mode))
    users_creation(db, users_mode)
    print("users_creation finished in mode " + str(users_mode))
    requests_creation(db, requests_mode)
    print("requests_creation finished in mode " + str(requests_mode))
    bot_data_creation(db, bot_data_mode)
    print("bot_data_creation finished in mode " + str(bot_data_mode))
