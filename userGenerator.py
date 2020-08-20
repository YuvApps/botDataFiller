import random
import calendar
from datetime import datetime
import copy
from bson import ObjectId


def get_user(user_id=0):
    if user_id == 0:
        user_id = random.randint(1, 999)

    friends = []
    for index in range(random.randint(3, 6)):
        friends.append("fake" + str(random.randint(1, 999)) + "@gmail.com")

    new_user = {
        "firstName": "fakeFirst" + str(user_id),
        "lastName": "fakeLast" + str(user_id),
        "email": "fake" + str(user_id) + "@gmail.com",
        "password": "123456",
        "answerPassword": "dad",
        "phoneNumber": "0523456790",
        "yearOfBirth": random.randint(1960, 2010),
        "maritalStatus": random.randint(1, 5),  # 1 - single, 2 - Married, 3 - divorcee, 4 - widow, 5 - other
        "addictedStatus": random.randint(1, 10),
        "myTarget": random.randint(1000, 68000),
        "walletMember": True,
        "friendMember": True,
        "myWalletMembers": friends,
        "myFixedExpenses": [{"name": "Rent", "expense": random.randint(1, 10000)},
                            {"name": "Kids Schools", "expense": random.randint(1, 10000)},
                            {"name": "Car Rental", "expense": random.randint(1, 10000)}],
        "myFixedIncomes": [{"name": "Salary", "income": random.randint(8000, 36000)}],
        "passes": random.randint(0, 5),
        "creditCardId": "",
        "stripeCardId": ""
    }

    return new_user


# noinspection PyTypeChecker
def get_item(user):
    all_categories = get_all_categories()

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

        num_of_friends = len(user["myWalletMembers"])
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


def get_req_by_user(user):

    start_date = 1597912747202
    end_date = 1597912833769

    time_between_dates = end_date - start_date

    random_number_of_days = random.randrange(time_between_dates)
    random_date = start_date + random_number_of_days

    new_item = get_item(user)

    while new_item == {}:
        new_item = get_item(user)

    new_request = {
        "email": user["email"],
        "openDate": random_date,
        "closedDate": random_date,
        "category": new_item["category"],
        "subCategory": new_item["subCategory"],
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
            main_json["month"] = datetime.fromtimestamp(request["openDate"] / 1000).month
            main_json["month_complete"] = (
                round(datetime.fromtimestamp(
                    request["openDate"] / 1000).day / calendar.monthrange(2020, main_json["month"])[1], 2)
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


def get_all_questions():
    all_questions = [
        {
            "question": "How many times do you think you will use this product?",
            "level": 3,
            "possibleAnswers":
                [
                    {
                        "_id": ObjectId(),
                        "answer": "It is a disposable product ..",
                        "points": 9
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "I believe I will use it often",
                        "points": 7
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "I believe I will use it in cases of need. Always good to have, right?",
                        "points": 5
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "to be honest, I believe i wouldn’t use it that often",
                        "points": 3
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "I'll use it only for special occations",
                        "points": 2
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "I actually haven't thought about it",
                        "points": 1
                    }
                ]
        }, {
            "question": "Rate the importance of this product compared to other products this month?",
            "level": 3,
            "possibleAnswers":
                [
                    {
                        "_id": ObjectId(),
                        "answer": "it is a valauble item I'm not willing to give up on",
                        "points": 9
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "I believe it could be one of the most important "
                                  "things I'd buy or will buy this month",
                        "points": 7
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "its not very imporant, but also it is not insignificant",
                        "points": 5
                    },
                    {
                        "_id": ObjectId(),
                        "answer": "insignificant",
                        "points": 2
                    }
                ]
        }, {
            "question": "What is the purpose of this product?",
            "level": 3,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it is a valuable item im not willing to give up on",
                    "points": 9
                },
                {
                        "_id": ObjectId(),
                    "answer": "this products will improve my quality of life",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "this product will improve my distant future",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "the product will improve my near future",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "This product is only essintial for a week more or less",
                    "points": 2
                },
                {
                        "_id": ObjectId(),
                    "answer": "The product will be an improvement only for specific occetions",
                    "points": 1
                }
            ]
        }, {
            "question": "In two weeks from now, do you think you will  have the same desire to purchase this item?",
            "level": 3,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "not relevant, using this product is essetial for the next two weeks",
                    "points": 9
                },
                {
                        "_id": ObjectId(),
                    "answer": "almost certain",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "Im not certain, but I do believe so",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "almost certain I won't",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "Certainly not",
                    "points": 1
                }
            ]
        }, {
            "question": "do you believe buying this product will be justified in "
                        "case you exceed your own monthly budget?",
            "level": 3,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it is a valuable item im not willing to give up on",
                    "points": 9
                },
                {
                        "_id": ObjectId(),
                    "answer": "I find it necessary, therefore I do not mind overdrafting for it",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "the product is valuable, but I wouldn’t overdraft for it",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "no chance. Ill buy it only if I have enough resting money in my savings ",
                    "points": 2
                }
            ]
        }, {
            "question": "Is this product worth an overdraft in your bank account?",
            "level": 3,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it is a valuable item im not willing to give up on",
                    "points": 9
                },
                {
                        "_id": ObjectId(),
                    "answer": "I find it necessary, therefore I do not mind overdrafting for it",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "the product is valuable, but I wouldn’t overdraft for it",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "no chance. Ill buy it only if I have enough resting money in my savings ",
                    "points": 2
                }
            ]
        }, {
            "question": "What are you willing to give up for in order to buy this product?",
            "level": 3,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it is a necessary item, therefore I am willing to give what it takes to get it",
                    "points": 9
                },
                {
                        "_id": ObjectId(),
                    "answer": "I really want this product, and I'm willing to give up a lot for it",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "the product isnt highly important, therefore I will not give up much for it",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "the  product isnt important enough for me to invest in it",
                    "points": 2
                }
            ]
        }, {
            "question": "Are you sure you need this product?",
            "level": 3,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it is a valuable item im not willing to give up on",
                    "points": 9
                },
                {
                        "_id": ObjectId(),
                    "answer": "its not a necessity, but I really want it",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "its not necessary, but I would enjoy having it",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "I don’t need it, and I don’t want it",
                    "points": 2
                }
            ]
        }, {
            "question": "If you had company with you, would you have the same confidence to buy this product?",
            "level": 2,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "im not effected by friends that are with me when I shop",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "I believe so",
                    "points": 6
                },
                {
                        "_id": ObjectId(),
                    "answer": "im not certain, but I think so ",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "I might, and I might not",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "Probably not",
                    "points": 1
                }
            ]
        }, {
            "question": "When did you decide buy this product?",
            "level": 2,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "not relavant, I must buy this item today",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "I've been thinking about it for a while",
                    "points": 6
                },
                {
                        "_id": ObjectId(),
                    "answer": "Ive been thinking about it in the last few days",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "I've been thinking about it all day",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "I thought about it a few minutes ago",
                    "points": 1
                }
            ]
        }, {
            "question": "Do you own a similar product already?",
            "level": 2,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it’s a disposable product",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "No, I don’t have any product that is similar to it",
                    "points": 6
                },
                {
                        "_id": ObjectId(),
                    "answer": "Yes, it’s a product from the same catefory, but its very different",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "Yes, a similar product but not as good",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "yes, an identical product",
                    "points": 1
                }
            ]
        }, {
            "question": "How will this product improve your life?",
            "level": 2,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "it’s a necessary product, so obviously it will",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "this product will be a great upgrade in my life ",
                    "points": 6
                },
                {
                        "_id": ObjectId(),
                    "answer": "this product will improve my life ",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "this product will make my life a little easier",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "This product wont improve the quality of my life even a btt",
                    "points": 1
                }
            ]
        }, {
            "question": "How much efforts are you willing to make in order to own this product?",
            "level": 2,
            "possibleAnswers": [
                {
                        "_id": ObjectId(),
                    "answer": "I must have it, therefore I'll doas much as I can to gei it",
                    "points": 7
                },
                {
                        "_id": ObjectId(),
                    "answer": "Im willing to to make a lot of effort to get it, because it is worth it",
                    "points": 6
                },
                {
                        "_id": ObjectId(),
                    "answer": "willing to put an effort, but not too much",
                    "points": 5
                },
                {
                        "_id": ObjectId(),
                    "answer": "I'm only willing to put a bit effort",
                    "points": 3
                },
                {
                        "_id": ObjectId(),
                    "answer": "not willing to make any effort",
                    "points": 1
                }
            ]
        }
    ]

    return all_questions


def get_all_categories():
    all_categories = [
        {
            "category": "Groceries",
            "importance": 0.6,
            "subCategory": [
                {
                    "_id": ObjectId(),
                    "name": "General",
                    "importance": 0.5,
                    "items": []
                }, {
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
                    "_id": ObjectId(),
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
