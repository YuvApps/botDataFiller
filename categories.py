import pymongo

client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
categories_col = db["categories"]

json = [
    {
        "category": "Fun",
        "importance": 0.2
    }, {
        "category": "Attraction",
        "importance": 0.2
    }, {
        "category": "Activities",
        "importance": 0.2
    }, {
        "category": "Tech",
        "importance": 0.3
    }, {
        "category": "Home Design",
        "importance": 0.5
    }, {
        "category": "Food",
        "importance": 0.8
    }, {
        "category": "Drinks",
        "importance": 0.7
    }, {
        "category": "Cloths",
        "importance": 0.7
    }, {
        "category": "Fashion",
        "importance": 0.4
    }, {
        "category": "Cosmetics",
        "importance": 0.5
    }, {
        "category": "Furniture",
        "importance": 0.6
    }, {
        "category": "Medical",
        "importance": 0.9
    }, {
        "category": "Toys",
        "importance": 0.1
    }
]

categories_col.insert_many(json)

# categories_col.delete_many({})
