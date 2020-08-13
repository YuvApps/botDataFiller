import datetime
import random


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


def get_item():

    all_categories = get_all_categories()

    random_category = random.randint(0, len(all_categories))

    random_item = random.randint(0, len(all_categories[random_category]["items"]))

    new_item = {
        "category": all_categories[random_category]["category"],
        "cost": all_categories[random_category]["items"][random_item]["cost"],
        "necessity": all_categories[random_category]["items"][random_item]["necessity"],
        "friendsConfirmation": number,
        "botScore": number,
        "confirmationStatus": number
    }

    return new_item


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

    new_request = {
        "email": "fake" + str(user_id) + "@gmail.com",
        "openDate": random_date,
        "closedDate": random_date,
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


def get_all_categories():
    all_categories = [
        {
            "category": "Fun",
            "importance": 0.2,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Attraction",
            "importance": 0.2,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Activities",
            "importance": 0.2,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Tech",
            "importance": 0.3,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Home Design",
            "importance": 0.5,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Food",
            "importance": 0.8,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Drinks",
            "importance": 0.7,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Cloths",
            "importance": 0.7,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Fashion",
            "importance": 0.4,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Cosmetics",
            "importance": 0.5,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Furniture",
            "importance": 0.6,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Medical",
            "importance": 0.9,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }, {
            "category": "Toys",
            "importance": 0.1,
            "items": [
                {
                    "name": "",
                    "cost": 0,
                    "necessity": 0,
                }
            ]
        }
    ]

    return all_categories
