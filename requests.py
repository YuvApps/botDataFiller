import pymongo
import datetime
import random


start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 8, 1)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
requests_col = db["requests"]
req = {}
requests = []

for index in range(30000):
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    req["email"] = ""
    req["openDate"] = ""
    req["closedDate"] = ""
    req["category"] = ""
    req["cost"] = ""
    req["description"] = ""
    req["necessity"] = ""
    req["additionalDescription"] = ""
    req["pic"] = ""
    req["friendsConfirmation"] = ""
    req["botConfirmation"] = ""
    req["confirmationStatus"] = ""
    req["score"] = ""
    requests.append(req)

requests_col.delete_many({})

requests_col.insert_many(requests)
