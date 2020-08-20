from userGenerator import get_bot_data


def bot_data_creation(db, mode):
    if mode > 0:
        bot_data_col = db["bot_data"]
        users_col = db["users"]
        requests_col = db["requests"]

        if mode == 1:
            for index in range(10):
                all_json = get_bot_data(users_col, requests_col, index, index*100 + 99)
                bot_data_col.insert_many(all_json)
        else:
            bot_data_col.delete_many({})
