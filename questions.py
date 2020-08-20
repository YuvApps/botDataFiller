from userGenerator import get_all_questions


def questions_creation(db, mode):
    if mode > 0:
        questions_col = db["questions"]

        if mode == 1:
            json = get_all_questions()
            questions_col.insert_many(json)
        else:
            questions_col.delete_many({})
