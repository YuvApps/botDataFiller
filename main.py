import pymongo


def get_users_data(user_data, data_json):
    data_json["monthly_goals"] = user_data[""]
    data_json["category_spent"] = user_data[""]


def get_requests_data(request_data, extra,  data_json):
    data_json["category"] = request_data["category"]
    data_json["bot_score"] = request_data["botScore"]
    data_json["friends_approved"] = request_data["friendsConfirmation"]
    data_json["confirmation_status"] = request_data["confirmationStatus"]
    if request_data["category"] in extra:
        extra[request_data["category"]] = request_data["cost"]
    else:
        extra[request_data["category"]] = extra[request_data["category"]] + request_data["cost"]


if __name__ == '__main__':

    client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
    db = client["test"]
    bot_data_col = db["bot_data"]
    users_col = db["users"]
    requests_col = db["requests"]
    all_json = []

    json_structure = {
        "monthly_goals": 0.1,
        "category": 0.2,
        "bot_score": 68,
        "friends_approved": 0.75,
        "month_complete": 0.3,
        "category_spent": 0.3,
        "confirmation_status": 1
    }

    extra_data = {
        ""
    }

    for user in users_col.find({}):

        main_json = json_structure

        temp_json = []

        for request in requests_col.find({"email": user["email"]}):

            get_requests_data(request, extra_data, main_json)

            temp_json.append(main_json)

        for temp_req in temp_json:
            get_users_data(extra_data, main_json)

        all_json.append(temp_json)

    bot_data_col.insert_many(all_json)
    # my_col.delete_many({})
