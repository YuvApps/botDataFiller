from userGenerator import get_all_questions


def questions_creation(db, mode):
    if mode > 0:
        items_col = db["items"]

        if mode == 1:
            json = get_all_questions()
            items_col.insert_many(json)
        else:
            items_col.delete_many({})
