import random
from userGenerator import get_req_by_user


def requests_creation(db, mode):
    if mode > 0:
        requests_col = db["requests"]
        users_col = db["users"]
        requests_arr = []

        if mode == 1:
            for index in range(4000):
                requests_arr.append(get_req_by_user(users_col.find({"firstName": "fakeFirst" +
                                                                                 str(random.randint(1, 999))})[0]))

                print("request in index" + str(index) + " has finished")
                if len(requests_arr) % 1000 == 0:
                    requests_col.insert_many(requests_arr)
                    del requests_arr[:]

            requests_col.insert_many(requests_arr)
        else:
            requests_col.delete_many({})
