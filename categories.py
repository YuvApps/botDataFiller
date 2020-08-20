from userGenerator import get_all_categories


def categories_creation(db, mode):
    if mode > 0:
        categories_col = db["categories"]

        if mode == 1:
            json = get_all_categories()
            for category in json:
                for subCategory in category["subCategory"]:
                    del subCategory["items"]
            categories_col.insert_many(json)
        else:
            categories_col.delete_many({})
