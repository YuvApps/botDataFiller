from userGenerator import get_user


def users_creation(db, mode):
    if mode > 0:
        users_col = db["users"]
        users_arr = []

        if mode == 1:
            for index in range(1, 1000):
                users_arr.append(get_user(index))

            users_col.insert_many(users_arr)
        else:
            users_col.delete_many({})
