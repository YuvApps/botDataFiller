import datetime
import random
import calendar
import copy


def get_user(user_id=0):
    if user_id == 0:
        user_id = random.randint(1, 999)

    new_user = {
        "firstName": "fakeFirst" + str(user_id),
        "lastName": "fakeLast" + str(user_id),
        "email": "fake" + str(user_id) + "@gmail.com",
        "password": "123456",
        "answerPassword": "",
        "phoneNumber": "0523456790",
        "yearOfBirth": random.randint(1960, 2010),
        "maritalStatus": random.randint(1, 5),
        "addictedStatus": random.randint(1, 10),
        "myTarget": random.randint(1000, 68000),
        "walletMember": True,
        "friendMember": False,
        "myWalletMembers": [random.randint(1, 999),
                            random.randint(1, 999),
                            random.randint(1, 999)],
        "myFixedExpenses": [{"name": "Rent", "expense": random.randint(1, 10000)},
                            {"name": "Kids Schools", "expense": random.randint(1, 10000)},
                            {"name": "Car Rental", "expense": random.randint(1, 10000)}],
        "myFixedIncomes": [{"name": "Salary", "income": random.randint(8000, 36000)}],
        "passes": random.randint(0, 5)
    }

    return new_user


# noinspection PyTypeChecker
def get_item():
    all_categories = get_all_items()

    random_category_no = random.randint(0, len(all_categories) - 1)

    random_sub_category_no = random.randint(0, len(all_categories[random_category_no]["subCategory"]) - 1)

    if len(all_categories[random_category_no]["subCategory"][random_sub_category_no]["items"]) > 0:

        random_item_no = random.randint(0,
                                        len(all_categories[random_category_no]["subCategory"][random_sub_category_no][
                                                "items"]) - 1)

        total_importance = (
                                   all_categories[random_category_no]["importance"] * 2 +
                                   all_categories[random_category_no]["subCategory"][random_sub_category_no][
                                       "importance"]
                           ) / 3

        num_of_friends = random.randint(3, 6)
        friends_confirmations = []

        confirms_counter = 0

        for i in range(num_of_friends):
            confirm_status = True if random.random() < total_importance else False
            friends_confirmations.append({
                "email": "fake" + str(random.randint(1, 999)) + "@gmail.com",
                "confirm": confirm_status
            })
            if confirm_status:
                confirms_counter += 1

        confirms_per = confirms_counter / num_of_friends

        all_items = all_categories[random_category_no]["subCategory"][random_sub_category_no]["items"]
        selected_item_cost = all_items[random_item_no]['cost']

        new_item = {
            "category": all_categories[random_category_no]["category"],
            "subCategory": all_categories[random_category_no]["subCategory"][random_sub_category_no]["name"],
            "cost": selected_item_cost,
            "necessity": round(total_importance, 1) * 10,
            "friendsConfirmation": friends_confirmations,
            "botScore": round(100 * total_importance),
            "confirmationStatus":
                True if random.random() < max(total_importance ** 0.3, confirms_per ** 0.3) else False
        }

        return new_item
    return {}


def get_req_by_user(user_id=0):
    if user_id == 0:
        user_id = random.randint(1, 999)

    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 8, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    new_item = get_item()

    while new_item == {}:
        new_item = get_item()

    new_request = {
        "email": "fake" + str(user_id) + "@gmail.com",
        "openDate": random_date.strftime("%d/%m/%Y"),
        "closedDate": random_date.strftime("%d/%m/%Y"),
        "category": new_item["category"],
        "cost": new_item["cost"],
        "description": "",
        "necessity": new_item["necessity"],
        "additionalDescription": "",
        "pic": "",
        "friendsConfirmation": new_item["friendsConfirmation"],
        "botScore": new_item["botScore"],
        "confirmationStatus": new_item["confirmationStatus"]
    }

    return new_request


def get_bot_data(users_col, requests_col, begin_num, end_num):
    all_json = []

    json_structure = {
        "monthly_goals": 0.0,
        "item_importance": 0.0,
        "bot_score": 0,
        "friends_approved": 0.0,
        "month_complete": 0.0,
        "category_spent": 0,
        "confirmation_status": 0
    }

    extra_data = {}

    users = users_col.find({"firstName": {"$gt": "fakeFirst" + str(begin_num), "$lte": "fakeFirst" + str(end_num)}})

    for user in users:

        temp_json = []

        for request in requests_col.find({"email": user["email"]}):
            main_json = copy.deepcopy(json_structure)
            main_json["category"] = request["category"]
            main_json["item_importance"] = request["botScore"] / 100
            main_json["bot_score"] = request["botScore"]
            friends_counter = 0
            for friend in request["friendsConfirmation"]:
                if friend["confirm"]:
                    friends_counter += 1
            main_json["friends_approved"] = round(friends_counter / len(request["friendsConfirmation"]), 2)
            main_json["confirmation_status"] = 1 if request["confirmationStatus"] else 0
            main_json["month"] = int(request["openDate"][3:5])
            main_json["month_complete"] = (
                round(int(request["openDate"][:2]) / calendar.monthrange(2020, main_json["month"])[1], 2)
            )
            if main_json["month"] not in extra_data:
                extra_data[main_json["month"]] = {}
            if request["category"] not in extra_data[main_json["month"]]:
                extra_data[main_json["month"]][request["category"]] = request["cost"]
            else:
                extra_data[main_json["month"]][request["category"]] += request["cost"]

            temp_json.append(main_json)

        monthly_spent = {}

        for month in extra_data:
            monthly_spent[month] = 0
            for spent in extra_data[month].values():
                monthly_spent[month] += spent

        for temp_req in temp_json:
            temp_req["category_spent"] = \
                round(extra_data[temp_req["month"]][temp_req["category"]] / monthly_spent[temp_req["month"]], 2)
            temp_req["monthly_goals"] = \
                round((user["myTarget"] - monthly_spent[temp_req["month"]]) / user["myTarget"], 2)
            del temp_req["category"]
            del temp_req["month"]

        all_json += temp_json
        print("finished user:" + user["firstName"])

    return all_json


def get_all_items():
    all_categories = [
        {
            "category": "Groceries",
            "importance": 0.6,
            "subCategory": [
                {
                    "name": "General",
                    "importance": 0.5,
                    "items": []
                }, {
                    "name": "Food & Drinks",
                    "importance": 0.7,
                    "items": [
                        {
                            "name": "Milk",
                            "cost": 12
                        }, {
                            "name": "Bread",
                            "cost": 7
                        }, {
                            "name": "6 Beers",
                            "cost": 40
                        }, {
                            "name": "General Shopping",
                            "cost": 265
                        }, {
                            "name": "Bakery",
                            "cost": 40
                        }, {
                            "name": "Cornflakes",
                            "cost": 25
                        }, {
                            "name": "Vegetables And Fruits",
                            "cost": 36
                        }, {
                            "name": "Olive Oil",
                            "cost": 30
                        }, {
                            "name": "Hot Dish",
                            "cost": 9
                        }
                    ]
                }, {
                    "name": "Home & Clean",
                    "importance": 0.7,
                    "items": [
                        {
                            "name": "Shampoo And Soap",
                            "cost": 18
                        }, {
                            "name": "Cleaning Products",
                            "cost": 73
                        }, {
                            "name": "Handkerchiefs Package",
                            "cost": 12
                        }, {
                            "name": "Disposable Cups",
                            "cost": 5
                        }, {
                            "name": "Hygiene Products",
                            "cost": 35
                        }, {
                            "name": "Tampons",
                            "cost": 11
                        }
                    ]
                }, {
                    "name": "Medic",
                    "importance": 0.9,
                    "items": [
                        {
                            "name": "Optalgin",
                            "cost": 32
                        }, {
                            "name": "Norfn",
                            "cost": 12
                        }, {
                            "name": "Vautrin",
                            "cost": 80
                        }
                    ]
                }
            ]
        }, {
            "category": "Restaurants",
            "importance": 0.4,
            "subCategory": [
                {
                    "name": "General",
                    "importance": 0.6,
                    "items": [
                        {
                            "name": "A Steakhouse",
                            "cost": 150
                        }, {
                            "name": "Italian Restaurant",
                            "cost": 90
                        }, {
                            "name": "Arabic Restaurant",
                            "cost": 45
                        }
                    ]
                }
            ]
        }, {
            "category": "Entertainment & Sport",
            "importance": 0.5,
            "subCategory": [
                {
                    "name": "General Entertainment",
                    "importance": 0.4,
                    "items": [
                        {
                            "name": "Stand Up",
                            "cost": 90
                        }, {
                            "name": "Sitting At The Bar",
                            "cost": 115
                        }, {
                            "name": "Snooker Game",
                            "cost": 64
                        }, {
                            "name": "Party",
                            "cost": 210
                        }
                    ]
                }, {
                    "name": "General Sport",
                    "importance": 0.3,
                    "items": [
                        {
                            "name": "Basketball Game",
                            "cost": 68
                        }, {
                            "name": "Soccer Game",
                            "cost": 84
                        }, {
                            "name": "Tennis Game",
                            "cost": 34
                        }
                    ]
                }
            ]
        }, {
            "category": "Fashion",
            "importance": 0.3,
            "subCategory": [
                {
                    "name": "Clothing and Footwear",
                    "importance": 0.7,
                    "items": [
                        {
                            "name": "Shirt Ransom",
                            "cost": 350
                        }, {
                            "name": "Sports Shoes",
                            "cost": 390
                        }, {
                            "name": "Sundress",
                            "cost": 420
                        }, {
                            "name": "High Heels",
                            "cost": 200
                        }, {
                            "name": "Sun Hat",
                            "cost": 100
                        }
                    ]
                }, {
                    "name": "Fashion Accessories, Perfumes and Makeup",
                    "importance": 0.5,
                    "items": [
                        {
                            "name": "Bracelet",
                            "cost": 120
                        }, {
                            "name": "Chain",
                            "cost": 150
                        }, {
                            "name": "Ring",
                            "cost": 120
                        }, {
                            "name": "Perfume",
                            "cost": 350
                        }
                    ]
                }, {
                    "name": "Beauty & General Health Care",
                    "importance": 0.4,
                    "items": [
                        {
                            "name": "Mascara",
                            "cost": 30
                        }, {
                            "name": "Lipstick",
                            "cost": 12
                        }, {
                            "name": "Yoga Mat",
                            "cost": 80
                        }, {
                            "name": "Powder",
                            "cost": 20
                        }, {
                            "name": "Stick",
                            "cost": 10
                        }, {
                            "name": "Face Cream",
                            "cost": 40
                        }, {
                            "name": "Hand Cream",
                            "cost": 45
                        }
                    ]
                }
            ]
        }, {
            "category": "Gifts & Leisure",
            "importance": 0.2,
            "subCategory": [
                {
                    "name": "Attractions",
                    "importance": 0.3,
                    "items": [
                        {
                            "name": "The Biblical Zoo",
                            "cost": 30
                        }, {
                            "name": "Luna Park",
                            "cost": 50
                        }, {
                            "name": "Yes Planet",
                            "cost": 80
                        }, {
                            "name": "Municipal Pool",
                            "cost": 50
                        }, {
                            "name": "Pack Of Coffee",
                            "cost": 20
                        }, {
                            "name": "Room Escape",
                            "cost": 150
                        }, {
                            "name": "Winery",
                            "cost": 50
                        }
                    ]
                }, {
                    "name": "Gifts",
                    "importance": 0.2,
                    "items": [
                        {
                            "name": "Towel",
                            "cost": 20
                        }, {
                            "name": "Greeting Card",
                            "cost": 13
                        }, {
                            "name": "Football",
                            "cost": 100
                        }, {
                            "name": "Set Of Pots",
                            "cost": 200
                        }, {
                            "name": "Briefcase",
                            "cost": 230
                        }, {
                            "name": "Watch",
                            "cost": 800
                        }, {
                            "name": "Cards Abroad",
                            "cost": 1900
                        }, {
                            "name": "Flowers",
                            "cost": 200
                        }
                    ]
                }, {
                    "name": "Toys",
                    "importance": 0.1,
                    "items": [
                        {
                            "name": "Control Car",
                            "cost": 450
                        }, {
                            "name": "A Barbie Doll",
                            "cost": 200
                        }, {
                            "name": "Pop Doll",
                            "cost": 50
                        }
                    ]
                }
            ]
        }, {
            "category": "Vehicle & Transportation",
            "importance": 0.7,
            "subCategory": [
                {
                    "name": "Car Expenses",
                    "importance": 0.8,
                    "items": [
                        {
                            "name": "Fuel",
                            "cost": 250
                        }, {
                            "name": "Yearly Test",
                            "cost": 120
                        }
                    ]
                }, {
                    "name": "Public Transportation",
                    "importance": 0.8,
                    "items": [
                        {
                            "name": "Traveling To Vocation",
                            "cost": 50
                        }, {
                            "name": "Drive Home",
                            "cost": 20
                        }
                    ]
                }, {
                    "name": "Taxi",
                    "importance": 0.6,
                    "items": [
                        {
                            "name": "Traveling Friend",
                            "cost": 100
                        }
                    ]
                }
            ]
        }, {
            "category": "Other",
            "importance": 0.6,
            "subCategory": [
                {
                    "name": "Pet",
                    "importance": 0.7,
                    "items": [
                        {
                            "name": "Dog Food",
                            "cost": 350
                        }, {
                            "name": "Vaccinations",
                            "cost": 80
                        }, {
                            "name": "Dog Toys",
                            "cost": 210
                        }, {
                            "name": "Aquarium",
                            "cost": 1000
                        }
                    ]
                }, {
                    "name": "Baby",
                    "importance": 0.8,
                    "items": [
                        {
                            "name": "Diapers",
                            "cost": 90
                        }, {
                            "name": "Materna",
                            "cost": 20
                        }, {
                            "name": "Gerber",
                            "cost": 19
                        }
                    ]
                }
            ]
        }
    ]

    return all_categories
