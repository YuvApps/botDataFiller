from userGenerator import get_all_categories


def categories_creation(db, mode):
    if mode > 0:
        items_col = db["items"]

        if mode == 1:
            json = get_all_categories()
            for category in json:
                for subCategory in category["subCategory"]:
                    del subCategory["items"]
            items_col.insert_many(json)
        else:
            items_col.delete_many({})
