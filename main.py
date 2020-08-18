from users import users_creation
from items import items_creation
from requests import requests_creation
from bot_data import bot_data_creation

if __name__ == '__main__':
    users_mode = 0
    items_mode = 0
    requests_mode = 0
    bot_data_mode = 0

    users_creation(users_mode)
    print("users_creation finished in mode " + str(users_mode))
    items_creation(items_mode)
    print("items_creation finished in mode " + str(items_mode))
    requests_creation(requests_mode)
    print("requests_creation finished in mode " + str(requests_mode))
    bot_data_creation(bot_data_mode)
    print("bot_data_creation finished in mode " + str(bot_data_mode))
